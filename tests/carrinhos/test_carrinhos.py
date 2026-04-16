import pytest
from src.helpers.data_generator import gerar_usuario, gerar_produto
from src.helpers.contract_validator import validar_contrato
from src.models.schemas import CARRINHOS_LISTA_SCHEMA, CARRINHO_CRIADO_SCHEMA, CARRINHO_SCHEMA
from src.services.login_service import LoginService
from src.services.produto_service import ProdutoService
from src.services.carrinho_service import CarrinhoService


class TestListarCarrinhos:
    """Cenarios para GET /carrinhos."""

    @pytest.mark.smoke
    def test_listar_carrinhos_retorna_200(self, carrinho_service):
        resp = carrinho_service.listar_carrinhos()

        assert resp.status_code == 200
        assert "quantidade" in resp.json()

    @pytest.mark.contract
    def test_contrato_lista_carrinhos(self, carrinho_service):
        resp = carrinho_service.listar_carrinhos()

        validar_contrato(resp.json(), CARRINHOS_LISTA_SCHEMA)


class TestBuscarCarrinhoPorId:
    """Cenarios para GET /carrinhos/{id}."""

    @pytest.mark.regression
    def test_buscar_carrinho_por_id_retorna_200(
        self, usuario_service, produto_service, carrinho_service
    ):
        login_svc = LoginService()

        user_data = gerar_usuario()
        resp_user = usuario_service.cadastrar(user_data)
        user_id = resp_user.json()["_id"]
        token = login_svc.obter_token(user_data["email"], user_data["password"])

        prod_data = gerar_produto()
        resp_prod = produto_service.cadastrar(prod_data, token)
        prod_id = resp_prod.json()["_id"]

        payload = {"produtos": [{"idProduto": prod_id, "quantidade": 1}]}
        resp_criar = carrinho_service.cadastrar(payload, token)
        carrinho_id = resp_criar.json()["_id"]

        resp = carrinho_service.buscar_por_id(carrinho_id)

        assert resp.status_code == 200
        assert resp.json()["_id"] == carrinho_id

        carrinho_service.cancelar_compra(token)
        produto_service.excluir(prod_id, token)
        usuario_service.excluir(user_id)

    @pytest.mark.contract
    def test_contrato_buscar_carrinho_por_id(
        self, usuario_service, produto_service, carrinho_service
    ):
        login_svc = LoginService()

        user_data = gerar_usuario()
        resp_user = usuario_service.cadastrar(user_data)
        user_id = resp_user.json()["_id"]
        token = login_svc.obter_token(user_data["email"], user_data["password"])

        prod_data = gerar_produto()
        resp_prod = produto_service.cadastrar(prod_data, token)
        prod_id = resp_prod.json()["_id"]

        payload = {"produtos": [{"idProduto": prod_id, "quantidade": 1}]}
        resp_criar = carrinho_service.cadastrar(payload, token)
        carrinho_id = resp_criar.json()["_id"]

        resp = carrinho_service.buscar_por_id(carrinho_id)

        validar_contrato(resp.json(), CARRINHO_SCHEMA)

        carrinho_service.cancelar_compra(token)
        produto_service.excluir(prod_id, token)
        usuario_service.excluir(user_id)

    @pytest.mark.regression
    def test_buscar_carrinho_id_inexistente_retorna_400(self, carrinho_service):
        resp = carrinho_service.buscar_por_id("carrinho_inexiste")

        assert resp.status_code == 400


class TestCadastrarCarrinho:
    """Cenarios para POST /carrinhos."""

    @pytest.mark.smoke
    def test_cadastrar_carrinho_valido_retorna_201(
        self, usuario_service, produto_service, carrinho_service
    ):
        login_svc = LoginService()

        user_data = gerar_usuario()
        resp_user = usuario_service.cadastrar(user_data)
        user_id = resp_user.json()["_id"]
        token = login_svc.obter_token(user_data["email"], user_data["password"])

        prod_data = gerar_produto()
        resp_prod = produto_service.cadastrar(prod_data, token)
        prod_id = resp_prod.json()["_id"]

        payload = {"produtos": [{"idProduto": prod_id, "quantidade": 1}]}
        resp = carrinho_service.cadastrar(payload, token)

        assert resp.status_code == 201
        assert "Cadastro realizado com sucesso" in resp.json()["message"]

        carrinho_service.cancelar_compra(token)
        produto_service.excluir(prod_id, token)
        usuario_service.excluir(user_id)

    @pytest.mark.contract
    def test_contrato_carrinho_criado(
        self, usuario_service, produto_service, carrinho_service
    ):
        login_svc = LoginService()

        user_data = gerar_usuario()
        resp_user = usuario_service.cadastrar(user_data)
        user_id = resp_user.json()["_id"]
        token = login_svc.obter_token(user_data["email"], user_data["password"])

        prod_data = gerar_produto()
        resp_prod = produto_service.cadastrar(prod_data, token)
        prod_id = resp_prod.json()["_id"]

        payload = {"produtos": [{"idProduto": prod_id, "quantidade": 1}]}
        resp = carrinho_service.cadastrar(payload, token)

        validar_contrato(resp.json(), CARRINHO_CRIADO_SCHEMA)

        carrinho_service.cancelar_compra(token)
        produto_service.excluir(prod_id, token)
        usuario_service.excluir(user_id)

    @pytest.mark.regression
    def test_cadastrar_carrinho_sem_token_retorna_401(self, carrinho_service):
        payload = {"produtos": [{"idProduto": "qualquer", "quantidade": 1}]}
        resp = carrinho_service.cadastrar(payload, token=None)

        assert resp.status_code == 401

    @pytest.mark.regression
    def test_cadastrar_carrinho_produto_inexistente_retorna_400(
        self, carrinho_service, token_admin
    ):
        payload = {"produtos": [{"idProduto": "prod_invalido_xyz", "quantidade": 1}]}
        resp = carrinho_service.cadastrar(payload, token_admin)

        assert resp.status_code == 400

    @pytest.mark.regression
    def test_cadastrar_carrinho_duplicado_retorna_400(
        self, usuario_service, produto_service, carrinho_service
    ):
        """Cada usuario so pode ter um carrinho ativo."""
        login_svc = LoginService()

        user_data = gerar_usuario()
        resp_user = usuario_service.cadastrar(user_data)
        user_id = resp_user.json()["_id"]
        token = login_svc.obter_token(user_data["email"], user_data["password"])

        prod_data = gerar_produto()
        resp_prod = produto_service.cadastrar(prod_data, token)
        prod_id = resp_prod.json()["_id"]

        payload = {"produtos": [{"idProduto": prod_id, "quantidade": 1}]}
        carrinho_service.cadastrar(payload, token)

        prod_data2 = gerar_produto()
        resp_prod2 = produto_service.cadastrar(prod_data2, token)
        prod_id2 = resp_prod2.json()["_id"]

        payload2 = {"produtos": [{"idProduto": prod_id2, "quantidade": 1}]}
        resp = carrinho_service.cadastrar(payload2, token)

        assert resp.status_code == 400
        assert "Não é permitido ter mais de 1 carrinho" in resp.json()["message"]

        carrinho_service.cancelar_compra(token)
        produto_service.excluir(prod_id, token)
        produto_service.excluir(prod_id2, token)
        usuario_service.excluir(user_id)

    @pytest.mark.regression
    def test_cadastrar_carrinho_quantidade_insuficiente_retorna_400(
        self, usuario_service, produto_service, carrinho_service
    ):
        login_svc = LoginService()

        user_data = gerar_usuario()
        resp_user = usuario_service.cadastrar(user_data)
        user_id = resp_user.json()["_id"]
        token = login_svc.obter_token(user_data["email"], user_data["password"])

        prod_data = gerar_produto()
        prod_data["quantidade"] = 1
        resp_prod = produto_service.cadastrar(prod_data, token)
        prod_id = resp_prod.json()["_id"]

        payload = {"produtos": [{"idProduto": prod_id, "quantidade": 99999}]}
        resp = carrinho_service.cadastrar(payload, token)

        assert resp.status_code == 400

        produto_service.excluir(prod_id, token)
        usuario_service.excluir(user_id)


class TestConcluirCompra:
    """Cenarios para DELETE /carrinhos/concluir-compra."""

    @pytest.mark.regression
    def test_concluir_compra_com_carrinho_retorna_200(
        self, usuario_service, produto_service, carrinho_service
    ):
        login_svc = LoginService()

        user_data = gerar_usuario()
        resp_user = usuario_service.cadastrar(user_data)
        user_id = resp_user.json()["_id"]
        token = login_svc.obter_token(user_data["email"], user_data["password"])

        prod_data = gerar_produto()
        resp_prod = produto_service.cadastrar(prod_data, token)
        prod_id = resp_prod.json()["_id"]

        payload = {"produtos": [{"idProduto": prod_id, "quantidade": 1}]}
        carrinho_service.cadastrar(payload, token)

        resp = carrinho_service.concluir_compra(token)

        assert resp.status_code == 200
        assert "sucesso" in resp.json()["message"].lower()

        produto_service.excluir(prod_id, token)
        usuario_service.excluir(user_id)

    @pytest.mark.regression
    def test_concluir_compra_sem_carrinho_retorna_200(self, carrinho_service, token_admin):
        resp = carrinho_service.concluir_compra(token_admin)

        assert resp.status_code == 200

    @pytest.mark.regression
    def test_concluir_compra_sem_token_retorna_401(self, carrinho_service):
        resp = carrinho_service.concluir_compra(token=None)

        assert resp.status_code == 401


class TestCancelarCompra:
    """Cenarios para DELETE /carrinhos/cancelar-compra."""

    @pytest.mark.regression
    def test_cancelar_compra_com_carrinho_retorna_200(
        self, usuario_service, produto_service, carrinho_service
    ):
        login_svc = LoginService()

        user_data = gerar_usuario()
        resp_user = usuario_service.cadastrar(user_data)
        user_id = resp_user.json()["_id"]
        token = login_svc.obter_token(user_data["email"], user_data["password"])

        prod_data = gerar_produto()
        resp_prod = produto_service.cadastrar(prod_data, token)
        prod_id = resp_prod.json()["_id"]

        payload = {"produtos": [{"idProduto": prod_id, "quantidade": 1}]}
        carrinho_service.cadastrar(payload, token)

        resp = carrinho_service.cancelar_compra(token)

        assert resp.status_code == 200

        produto_service.excluir(prod_id, token)
        usuario_service.excluir(user_id)

    @pytest.mark.regression
    def test_cancelar_compra_sem_carrinho_retorna_200(self, carrinho_service, token_admin):
        resp = carrinho_service.cancelar_compra(token_admin)

        assert resp.status_code == 200

    @pytest.mark.regression
    def test_cancelar_compra_sem_token_retorna_401(self, carrinho_service):
        resp = carrinho_service.cancelar_compra(token=None)

        assert resp.status_code == 401
