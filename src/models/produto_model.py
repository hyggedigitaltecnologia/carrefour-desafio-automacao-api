from pydantic import BaseModel, ConfigDict


class ProdutoPayload(BaseModel):
    nome: str
    preco: int
    descricao: str
    quantidade: int


class ProdutoResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    nome: str
    preco: int
    descricao: str
    quantidade: int
    _id: str


class ProdutoListResponse(BaseModel):
    quantidade: int
    produtos: list[ProdutoResponse]


class ProdutoCriadoResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    message: str
    _id: str
