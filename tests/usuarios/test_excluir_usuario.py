import pytest
from src.helpers.data_generator import gerar_usuario


class TestExcluirUsuario:
    """Cenarios para DELETE /usuarios/{id}."""

    @pytest.mark.smoke
    def test_excluir_usuario_existente_retorna_200(self, usuario_service):
        dados = gerar_usuario()
        resp_criar = usuario_service.cadastrar(dados)
        usuario_id = resp_criar.json()["_id"]

        resp = usuario_service.excluir(usuario_id)

        assert resp.status_code == 200
        assert "Registro excluído com sucesso" in resp.json()["message"]

    @pytest.mark.regression
    def test_excluir_usuario_inexistente_retorna_200(self, usuario_service):
        resp = usuario_service.excluir("id_invalido_abc123")

        assert resp.status_code == 200
        assert "Nenhum registro excluído" in resp.json()["message"]

    @pytest.mark.regression
    def test_excluir_usuario_com_carrinho_retorna_400(
        self, usuario_service, carrinho_cadastrado
    ):
        # O usuario do carrinho_cadastrado tem um carrinho ativo
        # Precisamos descobrir o usuario_id associado ao token
        # A fixture carrinho_cadastrado usa token_admin que vem de usuario_admin
        # Nao podemos excluir porque a fixture cuida do cleanup
        # Vamos testar diretamente: criar usuario, criar carrinho, tentar excluir
        from src.services.login_service import LoginService
        from src.services.carrinho_service import CarrinhoService
        from src.services.produto_service import ProdutoService
        from src.helpers.data_generator import gerar_produto

        login_svc = LoginService()
        carrinho_svc = CarrinhoService()
        produto_svc = ProdutoService()

        dados_user = gerar_usuario()
        resp_user = usuario_service.cadastrar(dados_user)
        user_id = resp_user.json()["_id"]
        token = login_svc.obter_token(dados_user["email"], dados_user["password"])

        dados_prod = gerar_produto()
        resp_prod = produto_svc.cadastrar(dados_prod, token)
        prod_id = resp_prod.json()["_id"]

        payload_carrinho = {"produtos": [{"idProduto": prod_id, "quantidade": 1}]}
        carrinho_svc.cadastrar(payload_carrinho, token)

        resp_excluir = usuario_service.excluir(user_id)
        assert resp_excluir.status_code == 400
        assert "carrinho" in resp_excluir.json()["message"].lower()

        # cleanup
        carrinho_svc.cancelar_compra(token)
        produto_svc.excluir(prod_id, token)
        usuario_service.excluir(user_id)

    @pytest.mark.regression
    def test_usuario_excluido_nao_e_encontrado(self, usuario_service):
        dados = gerar_usuario()
        resp_criar = usuario_service.cadastrar(dados)
        usuario_id = resp_criar.json()["_id"]

        usuario_service.excluir(usuario_id)

        resp_buscar = usuario_service.buscar_por_id(usuario_id)
        assert resp_buscar.status_code == 400
