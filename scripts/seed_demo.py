import requests


API_URL = "http://127.0.0.1:8000"


def criar_usuario(nome, email, tipo_usuario):

    response = requests.post(
        f"{API_URL}/usuarios",
        json={
            "nome": nome,
            "email": email,
            "tipo_usuario": tipo_usuario,
        },
        timeout=5,
    )

    if response.status_code == 400:
        print(f"Usuário já existe: {email}")
        return None

    response.raise_for_status()

    usuario = response.json()

    print(
        f"Usuário criado: "
        f"{nome} → ID {usuario['id_usuario']}"
    )

    return usuario["id_usuario"]


def analisar_login(
    id_usuario,
    ip,
    pais,
    cidade,
    horario,
    conhecido_ip,
    conhecido_dispositivo,
):

    response = requests.post(
        f"{API_URL}/login/analisar",
        json={
            "id_usuario": id_usuario,
            "id_dispositivo": None,
            "ip_origem": ip,
            "pais": pais,
            "cidade": cidade,
            "horario": horario,
            "conhecido_ip": conhecido_ip,
            "conhecido_dispositivo": conhecido_dispositivo,
        },
        timeout=5,
    )

    response.raise_for_status()

    resultado = response.json()

    print(
        f"\nLogin analisado:"
        f"\n  Risco: {resultado['risco']['nivel']}"
        f"\n  Pontuação: {resultado['risco']['pontuacao']}"
        f"\n  Ação: {resultado['acao']}"
    )

    if resultado["risco"]["motivos"]:
        print("  Motivos:")

        for motivo in resultado["risco"]["motivos"]:
            print(f"    - {motivo}")

    return resultado


def main():

    print("=" * 50)
    print("SENTINELAI — DADOS DE DEMONSTRAÇÃO")
    print("=" * 50)


    # =====================================================
    # USUÁRIOS
    # =====================================================

    joao = criar_usuario(
        "João Silva",
        "joao.demo@sentinel.local",
        "ALUNO",
    )

    maria = criar_usuario(
        "Maria Santos",
        "maria.demo@sentinel.local",
        "PROFESSOR",
    )

    carlos = criar_usuario(
        "Carlos Oliveira",
        "carlos.demo@sentinel.local",
        "ALUNO",
    )


    # =====================================================
    # LOGIN NORMAL
    # =====================================================

    if joao:

        analisar_login(
            id_usuario=joao,
            ip="192.168.1.10",
            pais="Brasil",
            cidade="Cuiabá",
            horario="2026-09-22T10:30:00",
            conhecido_ip=True,
            conhecido_dispositivo=True,
        )


    # =====================================================
    # LOGIN SUSPEITO
    # =====================================================

    if maria:

        analisar_login(
            id_usuario=maria,
            ip="185.20.30.40",
            pais="Brasil",
            cidade="São Paulo",
            horario="2026-09-22T23:45:00",
            conhecido_ip=False,
            conhecido_dispositivo=True,
        )


    # =====================================================
    # LOGIN DE ALTO RISCO
    # =====================================================

    if carlos:

        analisar_login(
            id_usuario=carlos,
            ip="91.200.10.50",
            pais="Alemanha",
            cidade="Berlim",
            horario="2026-09-22T03:15:00",
            conhecido_ip=False,
            conhecido_dispositivo=False,
        )


    print("\n")
    print("=" * 50)
    print("DEMONSTRAÇÃO CONCLUÍDA")
    print("=" * 50)


if __name__ == "__main__":
    main()