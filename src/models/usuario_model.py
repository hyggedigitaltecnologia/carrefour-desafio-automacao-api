from pydantic import BaseModel, ConfigDict
from typing import Optional


class UsuarioPayload(BaseModel):
    nome: str
    email: str
    password: str
    administrador: str


class UsuarioResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    nome: str
    email: str
    password: str
    administrador: str
    _id: str


class UsuarioListResponse(BaseModel):
    quantidade: int
    usuarios: list[UsuarioResponse]


class UsuarioCriadoResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    message: str
    _id: str


class MensagemResponse(BaseModel):
    message: str
