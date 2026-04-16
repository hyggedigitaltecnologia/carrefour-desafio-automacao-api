import pytest
from src.helpers.contract_validator import validar_contrato
from src.models.schemas import USUARIO_SCHEMA


class TestBuscarUsuarioPorId:
    """Cenarios para GET /usuarios/{id}."""

    @pytest.mark.smoke
    def test_buscar_usuario_existente_retorna_200(self, usuario_service, usuario_admin):
        resp = usuario_service.buscar_por_id(usuario_admin["_id"])

        assert resp.status_code == 200

    @pytest.mark.regression
    def test_buscar_usuario_retorna_dados_corretos(self, usuario_service, usuario_admin):
        resp = usuario_service.buscar_por_id(usuario_admin["_id"])
        body = resp.json()

        assert body["nome"] == usuario_admin["nome"]
        assert body["email"] == usuario_admin["email"]

    @pytest.mark.contract
    def test_contrato_buscar_usuario(self, usuario_service, usuario_admin):
        resp = usuario_service.buscar_por_id(usuario_admin["_id"])

        validar_contrato(resp.json(), USUARIO_SCHEMA)

    @pytest.mark.regression
    def test_buscar_usuario_id_inexistente_retorna_400(self, usuario_service):
        resp = usuario_service.buscar_por_id("id_invalido_12345")

        assert resp.status_code == 400
