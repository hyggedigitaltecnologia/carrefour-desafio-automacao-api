from src.services.base_service import BaseService


class ProdutoService(BaseService):
    """Servico responsavel pelas operacoes de produtos."""

    ENDPOINT = "/produtos"

    def listar_produtos(self, params=None):
        return self.get(self.ENDPOINT, params=params)

    def buscar_por_id(self, produto_id: str):
        return self.get(f"{self.ENDPOINT}/{produto_id}")

    def cadastrar(self, payload: dict, token: str):
        return self.post(self.ENDPOINT, payload=payload, token=token)

    def editar(self, produto_id: str, payload: dict, token: str):
        return self.put(f"{self.ENDPOINT}/{produto_id}", payload=payload, token=token)

    def excluir(self, produto_id: str, token: str):
        return self.delete(f"{self.ENDPOINT}/{produto_id}", token=token)
