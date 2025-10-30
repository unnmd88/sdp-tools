from typing import Annotated

from annotated_types import MaxLen, MinLen
from pydantic import BaseModel, ConfigDict, EmailStr, Field

from users.organizations import Organizations
from users.roles import Roles


class CreateUser(BaseModel):
    # username: str = Field(..., min_length=3, max_length=20)

    model_config = ConfigDict(use_enum_values=True)
    first_name: Annotated[str, MaxLen(32), Field(default='')]
    last_name: Annotated[str, MaxLen(32), Field(default='')]
    username: Annotated[str, MinLen(3), MaxLen(20)]
    organization: Organizations
    email: Annotated[EmailStr, Field(default=None)]
    password: Annotated[str | bytes, Field(repr=False)]
    is_active: bool
    is_admin: bool
    is_superuser: bool
    role: Roles
    phone_number: Annotated[str, MaxLen(10), Field(default='')]
    telegram: Annotated[str, MaxLen(32), Field(default='')]
    description: Annotated[str, Field(default='')]


class UserFromDbFullSchema(CreateUser):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr | str
    password: Annotated[str | bytes, Field(repr=False), Field(exclude=True)]
