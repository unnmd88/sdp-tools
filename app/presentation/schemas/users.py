from typing import Annotated
from annotated_types import MaxLen, MinLen
from pydantic_core.core_schema import FieldValidationInfo
from pydantic import(
    BaseModel,
    BeforeValidator,
    ConfigDict,
    EmailStr,
    Field,
    field_validator,
)
from core.enums import Organizations, Roles
from core.security_policies.user import check_password_to_set_is_valid


# class BaseUserSchema(BaseModel):
#     first_name: Annotated[str, MaxLen(32), Field(default='')]
#     last_name: Annotated[str, MaxLen(32), Field(default='')]
#     username: str
#     email: EmailStr | None | str = None
#     is_active: bool
#     is_admin: bool
#     is_superuser: bool
#     role: Annotated[Roles, BeforeValidator(lambda val: Roles(val))]
#     organization: Annotated[
#         Organizations, BeforeValidator(lambda val: Organizations(val))
#     ]
#     phone_number: Annotated[str, MaxLen(10), Field(default='')]
#     telegram: Annotated[str, MaxLen(32), Field(default='')]
#     description: Annotated[str, Field(default='')]

class BaseUserSchema(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: EmailStr | None | str
    is_active: bool
    role: Roles
    organization: Organizations
    phone_number: str | None
    telegram: str | None
    description: str | None


class ResponseUserSchema(BaseUserSchema):
    model_config = ConfigDict(strict=True, extra='ignore')

    id: int


class CreateUserSchema(BaseUserSchema):
    model_config = ConfigDict(use_enum_values=True, strict=True, extra='forbid')

    password: Annotated[str, MinLen(4), MaxLen(32)]
    email: EmailStr | None | str
    username: Annotated[str, MinLen(4), MaxLen(16)]
    role: Annotated[Roles, BeforeValidator(lambda val: Roles(val))]
    organization: Annotated[
        Organizations, BeforeValidator(lambda val: Organizations(val))
    ]

    @field_validator('username')
    def username_alphanumeric(cls, v):
        assert v.isalnum(), 'username должен содержать буквы и цифры'
        return v

    @field_validator('password')
    def check_password(cls, v, info: FieldValidationInfo):
        assert v != info.data['username'], 'username и пароль не должны совпадать'
        if not check_password_to_set_is_valid:
            raise ValueError('Недопустимый пароль')
        return v


class UpdateUserSchema(BaseModel):
    model_config = ConfigDict(use_enum_values=True, strict=True, extra='forbid')

    subject_username: str
    first_name: Annotated[str | None, MaxLen(32), Field(default=None), Field(examples=['dsd', 'das'])]
    last_name: Annotated[str | None, MaxLen(32), Field(default=None)]
    username: Annotated[str | None, MinLen(3), MaxLen(32), Field(default=None)]
    email: EmailStr | None | str = None
    is_admin: bool | None = None
    is_superuser: bool | None = None
    role: Annotated[Roles | None, BeforeValidator(lambda val: Roles(val) if val else None), Field(default=None)]
    organization: Annotated[
        Organizations | None, BeforeValidator(lambda val: Organizations(val) if val else None), Field(default=None)
    ]
    phone_number: Annotated[str | None, MaxLen(10), Field(default=None)]
    telegram: Annotated[str | None, MaxLen(32), Field(default=None),]
    description: Annotated[str | None, Field(default=None)]


class ChangeUserPasswordSchema(BaseModel):
    model_config = ConfigDict(strict=True, extra='forbid')

    old_password: str
    new_password: str

    @field_validator('new_password')
    def check_password(cls, v, info: FieldValidationInfo):
        if v == info.data['old_password']:
            raise ValueError('Пароли не должны совпадать')
        if not check_password_to_set_is_valid:
            raise ValueError('Недопустимый пароль')
        return v