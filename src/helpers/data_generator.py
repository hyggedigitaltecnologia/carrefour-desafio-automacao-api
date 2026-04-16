import uuid
from faker import Faker

fake = Faker("pt_BR")


def gerar_usuario(administrador="true"):
    sufixo = uuid.uuid4().hex[:8]
    return {
        "nome": fake.name(),
        "email": f"auto_{sufixo}@teste.com",
        "password": fake.password(length=10),
        "administrador": administrador,
    }


def gerar_usuario_nao_admin():
    return gerar_usuario(administrador="false")


def gerar_produto():
    return {
        "nome": f"Produto {uuid.uuid4().hex[:10]}",
        "preco": fake.random_int(min=10, max=5000),
        "descricao": fake.sentence(nb_words=6),
        "quantidade": fake.random_int(min=1, max=500),
    }


def gerar_login(email: str, password: str):
    return {"email": email, "password": password}


def gerar_carrinho(produto_id: str, quantidade: int = 1):
    return {"produtos": [{"idProduto": produto_id, "quantidade": quantidade}]}
