import pytest
from src.helpers.data_generator import gerar_usuario, gerar_produto
from src.services.login_service import LoginService
from src.services.usuario_service import UsuarioService
from src.services.produto_service import ProdutoService
from src.services.carrinho_service import CarrinhoService


class TestFluxoCompraCompleto:
    """Testes E2E que simulam fluxos reais de negocio."""

    @pytest.mark.e2e
    def test_fluxo_cadastro_login_compra_e_conclusao(self):
        """Simula o ciclo completo: criar usuario -> login -> criar produto ->
        adicionar ao carrinho -> concluir compra -> verificar estado final."""
        usuario_svc = UsuarioService()
        login_svc = LoginService()
        produto_svc = ProdutoService()
        carrinho_svc = CarrinhoService()

        # 1. Cadastrar usuario administrador
        dados_usuario = gerar_usuario(administrador="true")
        resp_usuario = usuario_svc.cadastrar(dados_usuario)
        assert resp_usuario.status_code == 201
        user_id = resp_usuario.json()["_id"]

        # 2. Realizar login e obter token
        resp_login = login_svc.realizar_login({
            "email": dados_usuario["email"],
            "password": dados_usuario["password"],
        })
        assert resp_login.status_code == 200
        token = resp_login.json()["authorization"]
        assert token.startswith("Bearer ")

        # 3. Cadastrar produto
        dados_produto = gerar_produto()
        resp_produto = produto_svc.cadastrar(dados_produto, token)
        assert resp_produto.status_code == 201
        prod_id = resp_produto.json()["_id"]

        # 4. Adicionar produto ao carrinho
        payload_carrinho = {"produtos": [{"idProduto": prod_id, "quantidade": 2}]}
        resp_carrinho = carrinho_svc.cadastrar(payload_carrinho, token)
        assert resp_carrinho.status_code == 201

        # 5. Concluir compra
        resp_conclusao = carrinho_svc.concluir_compra(token)
        assert resp_conclusao.status_code == 200

        # 6. Verificar que o carrinho foi removido
        resp_sem_carrinho = carrinho_svc.concluir_compra(token)
        assert "Não foi encontrado carrinho" in resp_sem_carrinho.json()["message"]

        # cleanup
        produto_svc.excluir(prod_id, token)
        usuario_svc.excluir(user_id)

    @pytest.mark.e2e
    def test_fluxo_cadastro_login_compra_e_cancelamento(self):
        """Simula o ciclo de cancelamento: criar usuario -> login ->
        criar produto -> adicionar ao carrinho -> cancelar compra ->
        verificar que estoque foi restaurado."""
        usuario_svc = UsuarioService()
        login_svc = LoginService()
        produto_svc = ProdutoService()
        carrinho_svc = CarrinhoService()

        dados_usuario = gerar_usuario(administrador="true")
        resp_usuario = usuario_svc.cadastrar(dados_usuario)
        user_id = resp_usuario.json()["_id"]
        token = login_svc.obter_token(dados_usuario["email"], dados_usuario["password"])

        dados_produto = gerar_produto()
        qtd_original = dados_produto["quantidade"]
        resp_produto = produto_svc.cadastrar(dados_produto, token)
        prod_id = resp_produto.json()["_id"]

        qtd_compra = 3
        payload_carrinho = {"produtos": [{"idProduto": prod_id, "quantidade": qtd_compra}]}
        carrinho_svc.cadastrar(payload_carrinho, token)

        # Verificar que estoque foi reduzido
        resp_prod_durante = produto_svc.buscar_por_id(prod_id)
        assert resp_prod_durante.json()["quantidade"] == qtd_original - qtd_compra

        # Cancelar compra
        resp_cancel = carrinho_svc.cancelar_compra(token)
        assert resp_cancel.status_code == 200

        # Verificar que estoque foi restaurado
        resp_prod_apos = produto_svc.buscar_por_id(prod_id)
        assert resp_prod_apos.json()["quantidade"] == qtd_original

        # cleanup
        produto_svc.excluir(prod_id, token)
        usuario_svc.excluir(user_id)

    @pytest.mark.e2e
    def test_fluxo_crud_completo_usuario(self):
        """Ciclo CRUD completo de usuario: criar -> ler -> atualizar -> ler -> excluir -> verificar exclusao."""
        usuario_svc = UsuarioService()

        # CREATE
        dados = gerar_usuario()
        resp_criar = usuario_svc.cadastrar(dados)
        assert resp_criar.status_code == 201
        user_id = resp_criar.json()["_id"]

        # READ
        resp_ler = usuario_svc.buscar_por_id(user_id)
        assert resp_ler.status_code == 200
        assert resp_ler.json()["email"] == dados["email"]

        # UPDATE
        dados_atualizados = {
            "nome": "Nome Atualizado E2E",
            "email": dados["email"],
            "password": dados["password"],
            "administrador": "true",
        }
        resp_atualizar = usuario_svc.editar(user_id, dados_atualizados)
        assert resp_atualizar.status_code == 200

        # READ novamente para confirmar
        resp_confirmar = usuario_svc.buscar_por_id(user_id)
        assert resp_confirmar.json()["nome"] == "Nome Atualizado E2E"

        # DELETE
        resp_excluir = usuario_svc.excluir(user_id)
        assert resp_excluir.status_code == 200

        # Verificar que foi excluido
        resp_verificar = usuario_svc.buscar_por_id(user_id)
        assert resp_verificar.status_code == 400

    @pytest.mark.e2e
    def test_fluxo_crud_completo_produto(self):
        """Ciclo CRUD completo de produto: criar usuario admin -> login ->
        criar produto -> ler -> atualizar -> excluir."""
        usuario_svc = UsuarioService()
        login_svc = LoginService()
        produto_svc = ProdutoService()

        dados_usuario = gerar_usuario(administrador="true")
        resp_user = usuario_svc.cadastrar(dados_usuario)
        user_id = resp_user.json()["_id"]
        token = login_svc.obter_token(dados_usuario["email"], dados_usuario["password"])

        # CREATE produto
        dados_prod = gerar_produto()
        resp_criar = produto_svc.cadastrar(dados_prod, token)
        assert resp_criar.status_code == 201
        prod_id = resp_criar.json()["_id"]

        # READ
        resp_ler = produto_svc.buscar_por_id(prod_id)
        assert resp_ler.status_code == 200
        assert resp_ler.json()["nome"] == dados_prod["nome"]

        # UPDATE
        dados_atualizados = gerar_produto()
        resp_editar = produto_svc.editar(prod_id, dados_atualizados, token)
        assert resp_editar.status_code == 200

        # READ novamente
        resp_confirmar = produto_svc.buscar_por_id(prod_id)
        assert resp_confirmar.json()["nome"] == dados_atualizados["nome"]

        # DELETE
        resp_excluir = produto_svc.excluir(prod_id, token)
        assert resp_excluir.status_code == 200

        # cleanup
        usuario_svc.excluir(user_id)
