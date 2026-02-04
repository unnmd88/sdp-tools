from typing import Annotated
from annotated_types import MaxLen, MinLen
from pydantic_core.core_schema import FieldValidationInfo
from pydantic import (
    BaseModel,
    BeforeValidator,
    ConfigDict,
    EmailStr,
    Field,
    field_validator,
)
from domain.enums.unsorted import Organizations, Roles


class BaseUserSchema(BaseModel):
    model_config = ConfigDict(use_enum_values=True, extra="ignore")

    firstname: Annotated[str | None, Field(examples=[None, "Иван"])]
    lastname: Annotated[str | None, Field(examples=[None, "Иванов"])]
    username: Annotated[str, Field(examples=["user", "edward"])]
    email: EmailStr | None
    is_active: bool
    role: Roles
    organization: Organizations
    phone_number: Annotated[
        str | None,
        Field(examples=[None, "988 920 11 55", "988 920 11 55", "988-920-11-55"]),
    ]
    telegram: Annotated[str | None, Field(examples=[None, "@user", "@jondoe"])]
    description: str = ""


class ResponseUserSchema(BaseUserSchema):
    model_config = ConfigDict(strict=True, extra="ignore")

    id: int


class CreateUserSchema(BaseUserSchema):
    password: str
    role: Annotated[Roles, BeforeValidator(lambda val: Roles(val))]
    organization: Annotated[
        Organizations, BeforeValidator(lambda val: Organizations(val))
    ]


class UpdateUserSchema(BaseModel):
    model_config = ConfigDict(use_enum_values=True, strict=True, extra="forbid")

    subject_username: str
    first_name: Annotated[
        str | None, MaxLen(32), Field(default=None), Field(examples=["dsd", "das"])
    ]
    last_name: Annotated[str | None, MaxLen(32), Field(default=None)]
    username: Annotated[str | None, MinLen(3), MaxLen(32), Field(default=None)]
    email: EmailStr | None | str = None
    is_admin: bool | None = None
    is_superuser: bool | None = None
    role: Annotated[
        Roles | None,
        BeforeValidator(lambda val: Roles(val) if val else None),
        Field(default=None),
    ]
    organization: Annotated[
        Organizations | None,
        BeforeValidator(lambda val: Organizations(val) if val else None),
        Field(default=None),
    ]
    phone_number: Annotated[str | None, MaxLen(10), Field(default=None)]
    telegram: Annotated[
        str | None,
        MaxLen(32),
        Field(default=None),
    ]
    description: Annotated[str | None, Field(default=None)]


class ChangeUserPasswordBaseSchema(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")

    old_password: str
    new_password: str



class UpdatedPasswordByAdminResponse(BaseModel):
    model_config = ConfigDict(strict=True, extra="forbid")

    username: str
    new_password: str