from typing import Annotated

from pydantic import BaseModel, BeforeValidator, ConfigDict, EmailStr
from core.enums.organizations import Organizations
from core.enums.roles import Roles

ACCESS_TOKEN_TYPE = 'access'
REFRESH_TOKEN_TYPE = 'refresh'


class TokenInfo(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = 'Bearer'


class AuthSchema(BaseModel):
    model_config = ConfigDict(strict=True, extra='ignore')

    username: str
    password_plain: str


class AuthSchemaToValidate(AuthSchema):

    password_hashed: bytes


class UserSchema(BaseModel):
    model_config = ConfigDict(strict=True, extra='ignore')

    id: int
    username: str
    email: EmailStr | None | str = None
    is_active: bool
    is_admin: bool
    is_superuser: bool
    role: Annotated[Roles, BeforeValidator(lambda val: Roles(val))]
    organization: Annotated[
        Organizations, BeforeValidator(lambda val: Organizations(val))
    ]


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
