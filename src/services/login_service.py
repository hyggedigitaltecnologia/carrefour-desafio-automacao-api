from src.services.base_service import BaseService


class LoginService(BaseService):
    """Servico responsavel pelas operacoes de autenticacao."""

    ENDPOINT = "/login"

    def realizar_login(self, payload: dict):
        return self.post(self.ENDPOINT, payload=payload)

    def obter_token(self, email: str, password: str) -> str:
        resp = self.realizar_login({"email": email, "password": password})
        return resp.json().get("authorization", "")
