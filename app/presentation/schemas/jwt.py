from pydantic import BaseModel, ConfigDict, EmailStr

from domain.enums.unsorted import Roles, Organizations


ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"


class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"


class BasePayloadJWTSchema(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")

    user_id: int
    sub: str
    typ: str
    exp: int
    iat: int


class PayloadAccessJWTSchema(BasePayloadJWTSchema):
    model_config = ConfigDict(strict=True, extra="forbid")

    role: str | Roles
    organization: str | Organizations
    email: EmailStr | None


class PayloadRefreshJWTSchema(BasePayloadJWTSchema):
    pass
