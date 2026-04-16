import pytest
from src.helpers.data_generator import gerar_usuario


class TestEditarUsuario:
    """Cenarios para PUT /usuarios/{id}."""

    @pytest.mark.smoke
    def test_editar_usuario_existente_retorna_200(self, usuario_service, usuario_admin):
        dados_atualizados = {
            "nome": "Nome Atualizado Teste",
            "email": usuario_admin["email"],
            "password": usuario_admin["password"],
            "administrador": "true",
        }
        resp = usuario_service.editar(usuario_admin["_id"], dados_atualizados)

        assert resp.status_code == 200
        assert "Registro alterado com sucesso" in resp.json()["message"]

    @pytest.mark.regression
    def test_editar_usuario_altera_nome_corretamente(self, usuario_service, usuario_admin):
        novo_nome = "Nome Modificado QA"
        dados = {
            "nome": novo_nome,
            "email": usuario_admin["email"],
            "password": usuario_admin["password"],
            "administrador": "true",
        }
        usuario_service.editar(usuario_admin["_id"], dados)

        resp_busca = usuario_service.buscar_por_id(usuario_admin["_id"])
        assert resp_busca.json()["nome"] == novo_nome

    @pytest.mark.regression
    def test_editar_usuario_com_email_duplicado_retorna_400(
        self, usuario_service, usuario_admin, usuario_comum
    ):
        dados = {
            "nome": usuario_comum["nome"],
            "email": usuario_admin["email"],
            "password": usuario_comum["password"],
            "administrador": "false",
        }
        resp = usuario_service.editar(usuario_comum["_id"], dados)

        assert resp.status_code == 400

    @pytest.mark.regression
    def test_editar_usuario_id_inexistente_cria_novo(self, usuario_service):
        dados = gerar_usuario()
        resp = usuario_service.editar("id_que_nao_existe", dados)

        assert resp.status_code == 201
        assert "Cadastro realizado com sucesso" in resp.json()["message"]

        # cleanup
        usuario_service.excluir(resp.json()["_id"])

    @pytest.mark.regression
    def test_editar_usuario_sem_campo_obrigatorio_retorna_400(self, usuario_service, usuario_admin):
        dados_incompletos = {"nome": "Apenas Nome"}
        resp = usuario_service.editar(usuario_admin["_id"], dados_incompletos)

        assert resp.status_code == 400
