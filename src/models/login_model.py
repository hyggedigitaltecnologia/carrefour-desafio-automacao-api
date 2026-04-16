from pydantic import BaseModel, ConfigDict


class LoginPayload(BaseModel):
    email: str
    password: str


class LoginSucessoResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    message: str
    authorization: str


class LoginErroResponse(BaseModel):
    message: str
