from pydantic import BaseModel, ConfigDict


class ItemCarrinho(BaseModel):
    idProduto: str
    quantidade: int


class CarrinhoPayload(BaseModel):
    produtos: list[ItemCarrinho]


class CarrinhoItemResponse(BaseModel):
    idProduto: str
    quantidade: int
    precoUnitario: int


class CarrinhoResponse(BaseModel):
    produtos: list[CarrinhoItemResponse]
    precoTotal: int
    quantidadeTotal: int
    idUsuario: str
    _id: str


class CarrinhoListResponse(BaseModel):
    quantidade: int
    carrinhos: list[CarrinhoResponse]


class CarrinhoCriadoResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    message: str
    _id: str
