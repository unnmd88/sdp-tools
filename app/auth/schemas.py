from typing import Annotated

from pydantic import BaseModel, Field, ConfigDict, EmailStr, BeforeValidator

from users.organizations import Organizations
from users.roles import Roles

ACCESS_TOKEN_TYPE = 'access'
REFRESH_TOKEN_TYPE = 'refresh'


class TokenInfo(BaseModel):
    access_token: str
    # refresh_token: str
    token_type: str = 'Bearer'


class UserSchema(BaseModel):
    model_config = ConfigDict(strict=True, extra="ignore")

    id: int
    username: str
    email: EmailStr | None | str = None
    is_active: bool
    is_admin: bool
    is_superuser: bool
    role: Annotated[Roles, BeforeValidator(lambda val: Roles(val))]
    organization: Annotated[Organizations, BeforeValidator(lambda val: Organizations(val))]
