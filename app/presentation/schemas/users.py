from typing import Annotated
from annotated_types import MaxLen, MinLen

from pydantic import BaseModel, BeforeValidator, ConfigDict, EmailStr, Field
from core.enums import Organizations, Roles


class BaseUserSchema(BaseModel):
    first_name: Annotated[str, MaxLen(32), Field(default='')]
    last_name: Annotated[str, MaxLen(32), Field(default='')]
    username: str
    email: EmailStr | None | str = None
    is_active: bool
    is_admin: bool
    is_superuser: bool
    role: Annotated[Roles, BeforeValidator(lambda val: Roles(val))]
    organization: Annotated[
        Organizations, BeforeValidator(lambda val: Organizations(val))
    ]
    phone_number: Annotated[str, MaxLen(10), Field(default='')]
    telegram: Annotated[str, MaxLen(32), Field(default='')]
    description: Annotated[str, Field(default='')]


class ResponseUserSchema(BaseUserSchema):
    model_config = ConfigDict(strict=True, extra='ignore')

    id: int


class CreateUserSchema(BaseUserSchema):
    model_config = ConfigDict(use_enum_values=True, strict=True, extra='forbid')

    password: Annotated[str, MinLen(4), MaxLen(16)]


class UpdateUserSchema(BaseUserSchema):
    model_config = ConfigDict(use_enum_values=True, strict=True, extra='forbid')

    subject_username: str


class ChangeUserPasswordSchema(BaseModel):
    model_config = ConfigDict(strict=True, extra='forbid')

    subject_username: str
    current_password: str
    new_password: str
