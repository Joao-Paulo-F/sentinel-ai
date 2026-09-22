from app.database import get_connection
from app.models import Usuario, Dispositivo, Acesso


def criar_usuario(usuario: Usuario) -> int:
    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            INSERT INTO usuario (
                nome,
                email,
                tipo_usuario,
                status
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                usuario.nome,
                usuario.email,
                usuario.tipo_usuario,
                usuario.status,
            ),
        )

        connection.commit()
        return cursor.lastrowid

    finally:
        connection.close()


def criar_dispositivo(dispositivo: Dispositivo) -> int:
    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            INSERT INTO dispositivo (
                id_usuario,
                identificador,
                sistema_operacional,
                navegador
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                dispositivo.id_usuario,
                dispositivo.identificador,
                dispositivo.sistema_operacional,
                dispositivo.navegador,
            ),
        )

        connection.commit()
        return cursor.lastrowid

    finally:
        connection.close()


def registrar_acesso(acesso: Acesso) -> int:
    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            INSERT INTO acesso (
                id_usuario,
                id_dispositivo,
                ip_origem,
                pais,
                cidade,
                resultado
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                acesso.id_usuario,
                acesso.id_dispositivo,
                acesso.ip_origem,
                acesso.pais,
                acesso.cidade,
                acesso.resultado,
            ),
        )

        connection.commit()
        return cursor.lastrowid

    finally:
        connection.close()


def registrar_analise(
    id_acesso: int,
    pontuacao: int,
    nivel_risco: str,
    motivo: str,
) -> int:

    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            INSERT INTO analise_risco (
                id_acesso,
                pontuacao,
                nivel_risco,
                motivo
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                id_acesso,
                pontuacao,
                nivel_risco,
                motivo,
            ),
        )

        connection.commit()
        return cursor.lastrowid

    finally:
        connection.close()


def registrar_acao(
    id_analise: int,
    tipo_acao: str,
    descricao: str,
) -> int:

    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            INSERT INTO acao_seguranca (
                id_analise,
                tipo_acao,
                descricao
            )
            VALUES (?, ?, ?)
            """,
            (
                id_analise,
                tipo_acao,
                descricao,
            ),
        )

        connection.commit()
        return cursor.lastrowid

    finally:
        connection.close()


def buscar_usuario(id_usuario: int):

    connection = get_connection()

    try:
        return connection.execute(
            """
            SELECT *
            FROM usuario
            WHERE id_usuario = ?
            """,
            (id_usuario,),
        ).fetchone()

    finally:
        connection.close()


def buscar_acessos():

    connection = get_connection()

    try:
        return connection.execute(
            """
            SELECT
                a.id_acesso,
                a.id_usuario,
                a.id_dispositivo,
                a.data_hora,
                a.ip_origem,
                a.pais,
                a.cidade,
                a.resultado,
                ar.pontuacao,
                ar.nivel_risco,
                ar.motivo
            FROM acesso a
            LEFT JOIN analise_risco ar
                ON a.id_acesso = ar.id_acesso
            ORDER BY a.data_hora DESC
            """
        ).fetchall()

    finally:
        connection.close()