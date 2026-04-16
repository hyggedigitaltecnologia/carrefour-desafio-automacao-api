import json
import logging
import time
import requests
from src.config import BASE_URL, REQUEST_TIMEOUT

logger = logging.getLogger("serverest.api")


class BaseService:
    """Servico base com metodos HTTP reutilizaveis e logging de requisicoes."""

    def __init__(self):
        self.base_url = BASE_URL
        self.timeout = REQUEST_TIMEOUT

    def _headers(self, token=None):
        headers = {"Content-Type": "application/json"}
        if token:
            headers["Authorization"] = token
        return headers

    def _log_request(self, method, url, payload=None, params=None):
        logger.info("──────────────────────────────────────────")
        logger.info(">>> %s %s", method, url)
        if params:
            logger.info("    Query Params: %s", params)
        if payload:
            logger.info("    Request Body: %s", json.dumps(payload, ensure_ascii=False, indent=2))

    def _log_response(self, resp, duracao_ms):
        status = resp.status_code
        nivel = logger.info if status < 400 else logger.warning

        nivel("<<< %s %s (%dms)", status, resp.reason, duracao_ms)
        try:
            body = resp.json()
            nivel("    Response Body: %s", json.dumps(body, ensure_ascii=False, indent=2))
        except ValueError:
            nivel("    Response Body: %s", resp.text[:500])
        logger.info("──────────────────────────────────────────")

    def _executar(self, method, endpoint, payload=None, token=None, params=None):
        url = f"{self.base_url}{endpoint}"
        self._log_request(method, url, payload=payload, params=params)

        inicio = time.perf_counter()
        resp = requests.request(
            method=method,
            url=url,
            json=payload,
            headers=self._headers(token),
            params=params,
            timeout=self.timeout,
        )
        duracao_ms = int((time.perf_counter() - inicio) * 1000)

        self._log_response(resp, duracao_ms)
        return resp

    def get(self, endpoint, token=None, params=None):
        return self._executar("GET", endpoint, token=token, params=params)

    def post(self, endpoint, payload=None, token=None):
        return self._executar("POST", endpoint, payload=payload, token=token)

    def put(self, endpoint, payload=None, token=None):
        return self._executar("PUT", endpoint, payload=payload, token=token)

    def delete(self, endpoint, token=None):
        return self._executar("DELETE", endpoint, token=token)
