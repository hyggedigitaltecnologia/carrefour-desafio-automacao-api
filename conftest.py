import pytest
from src.services.login_service import LoginService
from src.services.usuario_service import UsuarioService
from src.services.produto_service import ProdutoService
from src.services.carrinho_service import CarrinhoService
from src.helpers.data_generator import gerar_usuario, gerar_produto


# ──────────────── Services ────────────────

@pytest.fixture(scope="session")
def login_service():
    return LoginService()


@pytest.fixture(scope="session")
def usuario_service():
    return UsuarioService()


@pytest.fixture(scope="session")
def produto_service():
    return ProdutoService()


@pytest.fixture(scope="session")
def carrinho_service():
    return CarrinhoService()


# ──────────────── Dados e Autenticacao ────────────────

@pytest.fixture
def usuario_admin(usuario_service):
    """Cria um usuario administrador e retorna seus dados. Remove ao final."""
    dados = gerar_usuario(administrador="true")
    resp = usuario_service.cadastrar(dados)
    body = resp.json()
    dados["_id"] = body.get("_id", "")
    yield dados
    usuario_service.excluir(dados["_id"])


@pytest.fixture
def usuario_comum(usuario_service):
    """Cria um usuario nao-admin e retorna seus dados. Remove ao final."""
    dados = gerar_usuario(administrador="false")
    resp = usuario_service.cadastrar(dados)
    body = resp.json()
    dados["_id"] = body.get("_id", "")
    yield dados
    usuario_service.excluir(dados["_id"])


@pytest.fixture
def token_admin(usuario_admin, login_service):
    """Retorna token JWT de um usuario administrador."""
    return login_service.obter_token(usuario_admin["email"], usuario_admin["password"])


@pytest.fixture
def token_comum(usuario_comum, login_service):
    """Retorna token JWT de um usuario nao-admin."""
    return login_service.obter_token(usuario_comum["email"], usuario_comum["password"])


@pytest.fixture
def produto_cadastrado(produto_service, token_admin):
    """Cria um produto e retorna seus dados. Remove ao final."""
    dados = gerar_produto()
    resp = produto_service.cadastrar(dados, token_admin)
    body = resp.json()
    dados["_id"] = body.get("_id", "")
    yield dados
    produto_service.excluir(dados["_id"], token_admin)


@pytest.fixture
def carrinho_cadastrado(carrinho_service, produto_cadastrado, token_admin):
    """Cria um carrinho com um produto e retorna seus dados. Cancela ao final."""
    payload = {
        "produtos": [
            {"idProduto": produto_cadastrado["_id"], "quantidade": 1}
        ]
    }
    resp = carrinho_service.cadastrar(payload, token_admin)
    body = resp.json()
    yield {"_id": body.get("_id", ""), "payload": payload, "token": token_admin}
    carrinho_service.cancelar_compra(token_admin)
