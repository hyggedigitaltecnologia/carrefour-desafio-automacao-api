import pytest
from src.helpers.contract_validator import validar_contrato
from src.models.schemas import LOGIN_SUCESSO_SCHEMA, LOGIN_ERRO_SCHEMA


class TestLoginComSucesso:
    """Cenarios de login com credenciais validas."""

    @pytest.mark.smoke
    def test_login_valido_retorna_200(self, login_service, usuario_admin):
        payload = {"email": usuario_admin["email"], "password": usuario_admin["password"]}
        resp = login_service.realizar_login(payload)

        assert resp.status_code == 200
        assert "Login realizado com sucesso" in resp.json()["message"]

    @pytest.mark.smoke
    def test_login_valido_retorna_token_bearer(self, login_service, usuario_admin):
        payload = {"email": usuario_admin["email"], "password": usuario_admin["password"]}
        resp = login_service.realizar_login(payload)

        token = resp.json()["authorization"]
        assert token.startswith("Bearer ")

    @pytest.mark.contract
    def test_contrato_login_sucesso(self, login_service, usuario_admin):
        payload = {"email": usuario_admin["email"], "password": usuario_admin["password"]}
        resp = login_service.realizar_login(payload)

        validar_contrato(resp.json(), LOGIN_SUCESSO_SCHEMA)


class TestLoginComFalha:
    """Cenarios de login com credenciais invalidas ou ausentes."""

    @pytest.mark.smoke
    def test_login_senha_incorreta_retorna_401(self, login_service, usuario_admin):
        payload = {"email": usuario_admin["email"], "password": "senhaErrada123"}
        resp = login_service.realizar_login(payload)

        assert resp.status_code == 401
        assert resp.json()["message"] == "Email e/ou senha inválidos"

    @pytest.mark.regression
    def test_login_email_nao_cadastrado_retorna_401(self, login_service):
        payload = {"email": "inexistente_xyz@dominio.com", "password": "qualquer123"}
        resp = login_service.realizar_login(payload)

        assert resp.status_code == 401

    @pytest.mark.regression
    def test_login_sem_campo_email_retorna_400(self, login_service):
        payload = {"password": "teste123"}
        resp = login_service.realizar_login(payload)

        assert resp.status_code == 400

    @pytest.mark.regression
    def test_login_sem_campo_senha_retorna_400(self, login_service):
        payload = {"email": "alguem@teste.com"}
        resp = login_service.realizar_login(payload)

        assert resp.status_code == 400

    @pytest.mark.regression
    def test_login_body_vazio_retorna_400(self, login_service):
        resp = login_service.realizar_login({})

        assert resp.status_code == 400

    @pytest.mark.contract
    def test_contrato_login_erro(self, login_service):
        payload = {"email": "naoexiste@teste.com", "password": "errada"}
        resp = login_service.realizar_login(payload)

        validar_contrato(resp.json(), LOGIN_ERRO_SCHEMA)


class TestLoginSeguranca:
    """Cenarios de seguranca no endpoint de login."""

    @pytest.mark.security
    def test_login_rejeita_sql_injection_no_email(self, login_service):
        payload = {"email": "' OR 1=1 --", "password": "qualquer"}
        resp = login_service.realizar_login(payload)

        assert resp.status_code in [400, 401]

    @pytest.mark.security
    def test_login_rejeita_xss_no_email(self, login_service):
        payload = {"email": "<script>alert(1)</script>", "password": "qualquer"}
        resp = login_service.realizar_login(payload)

        assert resp.status_code in [400, 401]

    @pytest.mark.security
    def test_login_campo_email_com_espacos_retorna_erro(self, login_service):
        payload = {"email": "   ", "password": "qualquer"}
        resp = login_service.realizar_login(payload)

        assert resp.status_code in [400, 401]
