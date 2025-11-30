from dataclasses import dataclass

from app.core.enums.organizations import Organizations
from app.core.enums.roles import Roles


@dataclass(frozen=True, slots=True, kw_only=True)
class UserEntity:
    id: int
    first_name: str
    last_name: str
    username: str
    organization: Organizations
    email: str | None
    password: str | bytes
    is_active: bool
    is_admin: bool
    is_superuser: bool
    role: Roles
    phone_number: str = ''
    telegram: str = ''
    description: str = ''



