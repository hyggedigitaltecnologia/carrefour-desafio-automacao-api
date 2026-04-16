from src.services.base_service import BaseService


class UsuarioService(BaseService):
    """Servico responsavel pelas operacoes de usuarios."""

    ENDPOINT = "/usuarios"

    def listar_usuarios(self, params=None):
        return self.get(self.ENDPOINT, params=params)

    def buscar_por_id(self, usuario_id: str):
        return self.get(f"{self.ENDPOINT}/{usuario_id}")

    def cadastrar(self, payload: dict):
        return self.post(self.ENDPOINT, payload=payload)

    def editar(self, usuario_id: str, payload: dict):
        return self.put(f"{self.ENDPOINT}/{usuario_id}", payload=payload)

    def excluir(self, usuario_id: str):
        return self.delete(f"{self.ENDPOINT}/{usuario_id}")
