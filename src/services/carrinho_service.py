from src.services.base_service import BaseService


class CarrinhoService(BaseService):
    """Servico responsavel pelas operacoes de carrinhos."""

    ENDPOINT = "/carrinhos"

    def listar_carrinhos(self, params=None):
        return self.get(self.ENDPOINT, params=params)

    def buscar_por_id(self, carrinho_id: str):
        return self.get(f"{self.ENDPOINT}/{carrinho_id}")

    def cadastrar(self, payload: dict, token: str):
        return self.post(self.ENDPOINT, payload=payload, token=token)

    def concluir_compra(self, token: str):
        return self.delete(f"{self.ENDPOINT}/concluir-compra", token=token)

    def cancelar_compra(self, token: str):
        return self.delete(f"{self.ENDPOINT}/cancelar-compra", token=token)
