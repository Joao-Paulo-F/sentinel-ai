from datetime import datetime

from fastapi import FastAPI, HTTPException

from app.database import initialize_database
from app.models import Usuario, Dispositivo, Acesso
from app.schemas import (
    UsuarioCreate,
    DispositivoCreate,
    LoginRequest,
)
from app.repositories import (
    criar_usuario,
    criar_dispositivo,
    registrar_acesso,
    registrar_analise,
    registrar_acao,
    buscar_usuario,
    buscar_acessos,
)
from app.risk_analysis import analyze_risk
from app.security import (
    determine_action,
    action_description,
)


app = FastAPI(
    title="SentinelAI",
    description=(
        "Sistema de detecção e resposta "
        "a anomalias de acesso."
    ),
    version="1.0.0",
)


@app.on_event("startup")
def startup():
    initialize_database()


@app.get("/")
def root():
    return {
        "sistema": "SentinelAI",
        "status": "online",
        "versao": "1.0.0",
    }


@app.post("/usuarios")
def cadastrar_usuario(usuario: UsuarioCreate):

    try:
        novo_usuario = Usuario(
            nome=usuario.nome,
            email=usuario.email,
            tipo_usuario=usuario.tipo_usuario,
        )

        id_usuario = criar_usuario(novo_usuario)

        return {
            "mensagem": "Usuário cadastrado com sucesso",
            "id_usuario": id_usuario,
        }

    except Exception as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )


@app.post("/dispositivos")
def cadastrar_dispositivo(
    dispositivo: DispositivoCreate,
):

    usuario = buscar_usuario(
        dispositivo.id_usuario
    )

    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado.",
        )

    novo_dispositivo = Dispositivo(
        id_usuario=dispositivo.id_usuario,
        identificador=dispositivo.identificador,
        sistema_operacional=(
            dispositivo.sistema_operacional
        ),
        navegador=dispositivo.navegador,
    )

    id_dispositivo = criar_dispositivo(
        novo_dispositivo
    )

    return {
        "mensagem": "Dispositivo cadastrado com sucesso",
        "id_dispositivo": id_dispositivo,
    }


@app.post("/login/analisar")
def analisar_login(login: LoginRequest):

    usuario = buscar_usuario(login.id_usuario)

    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado.",
        )

    try:
        login_time = datetime.fromisoformat(
            login.horario
        )
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=(
                "Formato de horário inválido. "
                "Use YYYY-MM-DDTHH:MM:SS."
            ),
        )

    # No MVP, utilizamos um perfil comportamental
    # padrão. Posteriormente isso poderá vir do banco.
    usual_start_hour = 7
    usual_end_hour = 22
    usual_country = "Brasil"

    resultado = analyze_risk(
        login_time=login_time,
        usual_start_hour=usual_start_hour,
        usual_end_hour=usual_end_hour,
        country=login.pais,
        usual_country=usual_country,
        known_device=login.conhecido_dispositivo,
        known_ip=login.conhecido_ip,
    )

    action = determine_action(
        resultado.level
    )

    descricao_acao = action_description(
        action,
        resultado.level,
        resultado.score,
    )

    acesso = Acesso(
        id_usuario=login.id_usuario,
        id_dispositivo=login.id_dispositivo,
        ip_origem=login.ip_origem,
        pais=login.pais,
        cidade=login.cidade,
        resultado=action,
    )

    id_acesso = registrar_acesso(acesso)

    motivo = (
        "; ".join(resultado.reasons)
        if resultado.reasons
        else "Nenhuma anomalia identificada."
    )

    id_analise = registrar_analise(
        id_acesso=id_acesso,
        pontuacao=resultado.score,
        nivel_risco=resultado.level,
        motivo=motivo,
    )

    id_acao = registrar_acao(
        id_analise=id_analise,
        tipo_acao=action,
        descricao=descricao_acao,
    )

    return {
        "id_acesso": id_acesso,
        "id_analise": id_analise,
        "id_acao": id_acao,
        "risco": {
            "pontuacao": resultado.score,
            "nivel": resultado.level,
            "motivos": resultado.reasons,
        },
        "acao": action,
        "descricao": descricao_acao,
    }


@app.get("/acessos")
def listar_acessos():

    acessos = buscar_acessos()

    return [
        dict(acesso)
        for acesso in acessos
    ]
