import pytest
from src.helpers.data_generator import gerar_usuario, gerar_produto
from src.helpers.contract_validator import validar_contrato
from src.models.schemas import (
    PRODUTOS_LISTA_SCHEMA,
    PRODUTO_SCHEMA,
    PRODUTO_CRIADO_SCHEMA,
)
from src.services.login_service import LoginService
from src.services.carrinho_service import CarrinhoService


class TestListarProdutos:
    """Cenarios para GET /produtos."""

    @pytest.mark.smoke
    def test_listar_produtos_retorna_200(self, produto_service):
        resp = produto_service.listar_produtos()

        assert resp.status_code == 200
        assert "quantidade" in resp.json()

    @pytest.mark.contract
    def test_contrato_lista_produtos(self, produto_service):
        resp = produto_service.listar_produtos()

        validar_contrato(resp.json(), PRODUTOS_LISTA_SCHEMA)

    @pytest.mark.regression
    def test_filtrar_produto_por_nome(self, produto_service, produto_cadastrado):
        resp = produto_service.listar_produtos(params={"nome": produto_cadastrado["nome"]})
        body = resp.json()

        assert body["quantidade"] >= 1

    @pytest.mark.regression
    def test_buscar_produto_por_id_retorna_200(self, produto_service, produto_cadastrado):
        resp = produto_service.buscar_por_id(produto_cadastrado["_id"])

        assert resp.status_code == 200
        assert resp.json()["nome"] == produto_cadastrado["nome"]

    @pytest.mark.contract
    def test_contrato_buscar_produto(self, produto_service, produto_cadastrado):
        resp = produto_service.buscar_por_id(produto_cadastrado["_id"])

        validar_contrato(resp.json(), PRODUTO_SCHEMA)

    @pytest.mark.regression
    def test_buscar_produto_inexistente_retorna_400(self, produto_service):
        resp = produto_service.buscar_por_id("id_produto_invalido_xyz")

        assert resp.status_code == 400


class TestCadastrarProduto:
    """Cenarios para POST /produtos."""

    @pytest.mark.smoke
    def test_cadastrar_produto_valido_retorna_201(self, produto_service, token_admin):
        dados = gerar_produto()
        resp = produto_service.cadastrar(dados, token_admin)

        assert resp.status_code == 201
        assert "Cadastro realizado com sucesso" in resp.json()["message"]

        produto_service.excluir(resp.json()["_id"], token_admin)

    @pytest.mark.contract
    def test_contrato_produto_criado(self, produto_service, token_admin):
        dados = gerar_produto()
        resp = produto_service.cadastrar(dados, token_admin)

        validar_contrato(resp.json(), PRODUTO_CRIADO_SCHEMA)

        produto_service.excluir(resp.json()["_id"], token_admin)

    @pytest.mark.regression
    def test_cadastrar_produto_sem_token_retorna_401(self, produto_service):
        dados = gerar_produto()
        resp = produto_service.cadastrar(dados, token=None)

        assert resp.status_code == 401

    @pytest.mark.regression
    def test_cadastrar_produto_com_token_invalido_retorna_401(self, produto_service):
        dados = gerar_produto()
        resp = produto_service.cadastrar(dados, token="Bearer tokeninvalido123")

        assert resp.status_code == 401

    @pytest.mark.regression
    def test_cadastrar_produto_nome_duplicado_retorna_400(
        self, produto_service, token_admin, produto_cadastrado
    ):
        dados = gerar_produto()
        dados["nome"] = produto_cadastrado["nome"]
        resp = produto_service.cadastrar(dados, token_admin)

        assert resp.status_code == 400
        assert "já existe" in resp.json()["message"].lower()

    @pytest.mark.regression
    def test_cadastrar_produto_sem_campo_nome_retorna_400(self, produto_service, token_admin):
        dados = gerar_produto()
        del dados["nome"]
        resp = produto_service.cadastrar(dados, token_admin)

        assert resp.status_code == 400

    @pytest.mark.regression
    def test_cadastrar_produto_usuario_nao_admin_retorna_403(self, produto_service, token_comum):
        dados = gerar_produto()
        resp = produto_service.cadastrar(dados, token_comum)

        assert resp.status_code == 403


class TestEditarProduto:
    """Cenarios para PUT /produtos/{id}."""

    @pytest.mark.regression
    def test_editar_produto_existente_retorna_200(
        self, produto_service, token_admin, produto_cadastrado
    ):
        dados = gerar_produto()
        resp = produto_service.editar(produto_cadastrado["_id"], dados, token_admin)

        assert resp.status_code == 200

    @pytest.mark.regression
    def test_editar_produto_sem_token_retorna_401(self, produto_service, produto_cadastrado):
        dados = gerar_produto()
        resp = produto_service.editar(produto_cadastrado["_id"], dados, token=None)

        assert resp.status_code == 401

    @pytest.mark.regression
    def test_editar_produto_id_invalido_retorna_400(self, produto_service, token_admin):
        dados = gerar_produto()
        resp = produto_service.editar("id_inexistente_prod", dados, token_admin)

        assert resp.status_code == 400

    @pytest.mark.regression
    def test_editar_produto_nome_duplicado_retorna_400(
        self, produto_service, token_admin, produto_cadastrado
    ):
        dados = gerar_produto()
        resp_outro = produto_service.cadastrar(dados, token_admin)
        outro_id = resp_outro.json()["_id"]

        dados_dup = gerar_produto()
        dados_dup["nome"] = produto_cadastrado["nome"]
        resp = produto_service.editar(outro_id, dados_dup, token_admin)

        assert resp.status_code == 400
        assert "já existe" in resp.json()["message"].lower()

        produto_service.excluir(outro_id, token_admin)

    @pytest.mark.regression
    def test_editar_produto_usuario_nao_admin_retorna_403(
        self, produto_service, token_comum, produto_cadastrado
    ):
        dados = gerar_produto()
        resp = produto_service.editar(produto_cadastrado["_id"], dados, token_comum)

        assert resp.status_code == 403


class TestExcluirProduto:
    """Cenarios para DELETE /produtos/{id}."""

    @pytest.mark.regression
    def test_excluir_produto_existente_retorna_200(self, produto_service, token_admin):
        dados = gerar_produto()
        resp_criar = produto_service.cadastrar(dados, token_admin)
        prod_id = resp_criar.json()["_id"]

        resp = produto_service.excluir(prod_id, token_admin)

        assert resp.status_code == 200
        assert "Registro excluído com sucesso" in resp.json()["message"]

    @pytest.mark.regression
    def test_excluir_produto_sem_token_retorna_401(self, produto_service, produto_cadastrado):
        resp = produto_service.excluir(produto_cadastrado["_id"], token=None)

        assert resp.status_code == 401

    @pytest.mark.regression
    def test_excluir_produto_id_invalido_retorna_400(self, produto_service, token_admin):
        resp = produto_service.excluir("prod_id_nao_existe", token_admin)

        assert resp.status_code == 400

    @pytest.mark.regression
    def test_excluir_produto_que_faz_parte_de_carrinho_retorna_400(
        self, usuario_service, produto_service
    ):
        """Swagger: 400 - Produto faz parte de carrinho."""
        login_svc = LoginService()
        carrinho_svc = CarrinhoService()

        user_data = gerar_usuario()
        resp_user = usuario_service.cadastrar(user_data)
        user_id = resp_user.json()["_id"]
        token = login_svc.obter_token(user_data["email"], user_data["password"])

        prod_data = gerar_produto()
        resp_prod = produto_service.cadastrar(prod_data, token)
        prod_id = resp_prod.json()["_id"]

        payload = {"produtos": [{"idProduto": prod_id, "quantidade": 1}]}
        carrinho_svc.cadastrar(payload, token)

        resp = produto_service.excluir(prod_id, token)

        assert resp.status_code == 400
        assert "parte de carrinho" in resp.json()["message"].lower()

        # cleanup
        carrinho_svc.cancelar_compra(token)
        produto_service.excluir(prod_id, token)
        usuario_service.excluir(user_id)

    @pytest.mark.regression
    def test_excluir_produto_usuario_nao_admin_retorna_403(
        self, produto_service, token_comum, produto_cadastrado
    ):
        resp = produto_service.excluir(produto_cadastrado["_id"], token_comum)

        assert resp.status_code == 403
