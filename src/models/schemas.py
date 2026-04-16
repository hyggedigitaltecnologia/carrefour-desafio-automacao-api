"""
Schemas JSON para validacao de contrato das respostas da API ServeRest.
Utiliza jsonschema (Draft-07) para garantir a estrutura das respostas.
"""

LOGIN_SUCESSO_SCHEMA = {
    "type": "object",
    "properties": {
        "message": {"type": "string"},
        "authorization": {"type": "string"},
    },
    "required": ["message", "authorization"],
    "additionalProperties": False,
}

LOGIN_ERRO_SCHEMA = {
    "type": "object",
    "properties": {
        "message": {"type": "string"},
    },
    "required": ["message"],
}

USUARIO_SCHEMA = {
    "type": "object",
    "properties": {
        "nome": {"type": "string"},
        "email": {"type": "string"},
        "password": {"type": "string"},
        "administrador": {"type": "string"},
        "_id": {"type": "string"},
    },
    "required": ["nome", "email", "password", "administrador", "_id"],
}

USUARIOS_LISTA_SCHEMA = {
    "type": "object",
    "properties": {
        "quantidade": {"type": "integer"},
        "usuarios": {
            "type": "array",
            "items": USUARIO_SCHEMA,
        },
    },
    "required": ["quantidade", "usuarios"],
}

USUARIO_CRIADO_SCHEMA = {
    "type": "object",
    "properties": {
        "message": {"type": "string"},
        "_id": {"type": "string"},
    },
    "required": ["message", "_id"],
    "additionalProperties": False,
}

MENSAGEM_SCHEMA = {
    "type": "object",
    "properties": {
        "message": {"type": "string"},
    },
    "required": ["message"],
}

PRODUTO_SCHEMA = {
    "type": "object",
    "properties": {
        "nome": {"type": "string"},
        "preco": {"type": "integer"},
        "descricao": {"type": "string"},
        "quantidade": {"type": "integer"},
        "_id": {"type": "string"},
    },
    "required": ["nome", "preco", "descricao", "quantidade", "_id"],
}

PRODUTOS_LISTA_SCHEMA = {
    "type": "object",
    "properties": {
        "quantidade": {"type": "integer"},
        "produtos": {
            "type": "array",
            "items": PRODUTO_SCHEMA,
        },
    },
    "required": ["quantidade", "produtos"],
}

PRODUTO_CRIADO_SCHEMA = {
    "type": "object",
    "properties": {
        "message": {"type": "string"},
        "_id": {"type": "string"},
    },
    "required": ["message", "_id"],
    "additionalProperties": False,
}

CARRINHO_ITEM_SCHEMA = {
    "type": "object",
    "properties": {
        "idProduto": {"type": "string"},
        "quantidade": {"type": "integer"},
        "precoUnitario": {"type": "integer"},
    },
    "required": ["idProduto", "quantidade", "precoUnitario"],
}

CARRINHO_SCHEMA = {
    "type": "object",
    "properties": {
        "produtos": {"type": "array", "items": CARRINHO_ITEM_SCHEMA},
        "precoTotal": {"type": "integer"},
        "quantidadeTotal": {"type": "integer"},
        "idUsuario": {"type": "string"},
        "_id": {"type": "string"},
    },
    "required": ["produtos", "precoTotal", "quantidadeTotal", "idUsuario", "_id"],
}

CARRINHOS_LISTA_SCHEMA = {
    "type": "object",
    "properties": {
        "quantidade": {"type": "integer"},
        "carrinhos": {
            "type": "array",
            "items": CARRINHO_SCHEMA,
        },
    },
    "required": ["quantidade", "carrinhos"],
}

CARRINHO_CRIADO_SCHEMA = {
    "type": "object",
    "properties": {
        "message": {"type": "string"},
        "_id": {"type": "string"},
    },
    "required": ["message", "_id"],
    "additionalProperties": False,
}
