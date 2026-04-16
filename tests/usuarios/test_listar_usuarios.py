import pytest
from src.helpers.contract_validator import validar_contrato
from src.models.schemas import USUARIOS_LISTA_SCHEMA


class TestListarUsuarios:
    """Cenarios para GET /usuarios."""

    @pytest.mark.smoke
    def test_listar_usuarios_retorna_200(self, usuario_service):
        resp = usuario_service.listar_usuarios()

        assert resp.status_code == 200

    @pytest.mark.smoke
    def test_listar_usuarios_retorna_quantidade(self, usuario_service):
        resp = usuario_service.listar_usuarios()
        body = resp.json()

        assert "quantidade" in body
        assert isinstance(body["quantidade"], int)
        assert body["quantidade"] >= 0

    @pytest.mark.contract
    def test_contrato_lista_usuarios(self, usuario_service):
        resp = usuario_service.listar_usuarios()

        validar_contrato(resp.json(), USUARIOS_LISTA_SCHEMA)

    @pytest.mark.regression
    def test_filtrar_usuario_por_nome(self, usuario_service, usuario_admin):
        resp = usuario_service.listar_usuarios(params={"nome": usuario_admin["nome"]})
        body = resp.json()

        assert resp.status_code == 200
        assert body["quantidade"] >= 1
        assert any(u["nome"] == usuario_admin["nome"] for u in body["usuarios"])

    @pytest.mark.regression
    def test_filtrar_usuario_por_email(self, usuario_service, usuario_admin):
        resp = usuario_service.listar_usuarios(params={"email": usuario_admin["email"]})
        body = resp.json()

        assert resp.status_code == 200
        assert body["quantidade"] == 1
        assert body["usuarios"][0]["email"] == usuario_admin["email"]

    @pytest.mark.regression
    def test_filtrar_usuario_inexistente_retorna_lista_vazia(self, usuario_service):
        resp = usuario_service.listar_usuarios(params={"nome": "UsuarioQueNaoExisteABC123"})
        body = resp.json()

        assert resp.status_code == 200
        assert body["quantidade"] == 0
        assert body["usuarios"] == []

    @pytest.mark.regression
    def test_filtrar_por_administrador(self, usuario_service, usuario_admin):
        resp = usuario_service.listar_usuarios(params={"administrador": "true"})
        body = resp.json()

        assert resp.status_code == 200
        assert all(u["administrador"] == "true" for u in body["usuarios"])
