from pydantic import BaseModel, ConfigDict, EmailStr

from core.enums import Roles, Organizations


ACCESS_TOKEN_TYPE = 'access'
REFRESH_TOKEN_TYPE = 'refresh'


class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = 'Bearer'


class PayloadJWTSchema(BaseModel):
    model_config = ConfigDict(strict=True, extra='forbid')
    user_id: int
    sub: str
    role: str | Roles
    is_admin: bool
    is_superuser: bool
    organization: str | Organizations
    email: EmailStr | str
    typ: str
    exp: int
    iat: int
