import pytest
from src.helpers.data_generator import gerar_usuario
from src.helpers.contract_validator import validar_contrato
from src.models.schemas import USUARIO_CRIADO_SCHEMA


class TestCadastrarUsuario:
    """Cenarios para POST /usuarios."""

    @pytest.mark.smoke
    def test_cadastrar_usuario_valido_retorna_201(self, usuario_service):
        dados = gerar_usuario()
        resp = usuario_service.cadastrar(dados)

        assert resp.status_code == 201
        assert "Cadastro realizado com sucesso" in resp.json()["message"]

        usuario_service.excluir(resp.json()["_id"])

    @pytest.mark.contract
    def test_contrato_usuario_criado(self, usuario_service):
        dados = gerar_usuario()
        resp = usuario_service.cadastrar(dados)

        validar_contrato(resp.json(), USUARIO_CRIADO_SCHEMA)

        usuario_service.excluir(resp.json()["_id"])

    @pytest.mark.regression
    def test_cadastrar_usuario_nao_admin(self, usuario_service):
        dados = gerar_usuario(administrador="false")
        resp = usuario_service.cadastrar(dados)

        assert resp.status_code == 201

        usuario_service.excluir(resp.json()["_id"])

    @pytest.mark.regression
    def test_cadastrar_usuario_email_duplicado_retorna_400(self, usuario_service, usuario_admin):
        dados = gerar_usuario()
        dados["email"] = usuario_admin["email"]
        resp = usuario_service.cadastrar(dados)

        assert resp.status_code == 400
        assert "já está sendo usado" in resp.json()["message"]


class TestCadastrarUsuarioCamposObrigatorios:
    """Validacao de campos obrigatorios no cadastro."""

    @pytest.mark.regression
    def test_cadastrar_sem_nome_retorna_400(self, usuario_service):
        dados = gerar_usuario()
        del dados["nome"]
        resp = usuario_service.cadastrar(dados)

        assert resp.status_code == 400

    @pytest.mark.regression
    def test_cadastrar_sem_email_retorna_400(self, usuario_service):
        dados = gerar_usuario()
        del dados["email"]
        resp = usuario_service.cadastrar(dados)

        assert resp.status_code == 400

    @pytest.mark.regression
    def test_cadastrar_sem_password_retorna_400(self, usuario_service):
        dados = gerar_usuario()
        del dados["password"]
        resp = usuario_service.cadastrar(dados)

        assert resp.status_code == 400

    @pytest.mark.regression
    def test_cadastrar_sem_administrador_retorna_400(self, usuario_service):
        dados = gerar_usuario()
        del dados["administrador"]
        resp = usuario_service.cadastrar(dados)

        assert resp.status_code == 400

    @pytest.mark.regression
    def test_cadastrar_body_vazio_retorna_400(self, usuario_service):
        resp = usuario_service.cadastrar({})

        assert resp.status_code == 400


class TestCadastrarUsuarioValidacaoEmail:
    """Validacao de formato de email no cadastro."""

    @pytest.mark.regression
    @pytest.mark.parametrize("email_invalido", [
        "email-sem-arroba",
        "email@",
        "@semdominio.com",
        "email com espaco@teste.com",
        "",
    ])
    def test_cadastrar_com_email_invalido_retorna_400(self, usuario_service, email_invalido):
        dados = gerar_usuario()
        dados["email"] = email_invalido
        resp = usuario_service.cadastrar(dados)

        assert resp.status_code == 400
