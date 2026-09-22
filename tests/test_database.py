from app.models import Usuario
from app.repositories import criar_usuario


def test_criar_usuario():
    usuario = Usuario(
        nome="Usuário Teste",
        email="teste@instituicao.edu.br",
        tipo_usuario="ALUNO",
    )

    id_usuario = criar_usuario(usuario)

    assert id_usuario is not None
    assert id_usuario > 0