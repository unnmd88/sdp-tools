from typing import Annotated

from pydantic import BaseModel, BeforeValidator, ConfigDict, EmailStr
from core.enums import Organizations, Roles


class AuthSchema(BaseModel):
    model_config = ConfigDict(strict=True, extra='ignore')

    username: str
    password_plain: str


class AuthSchemaToValidate(AuthSchema):
    password_hashed: bytes
