from dataclasses import dataclass

from core.enums import Roles, Organizations


@dataclass(kw_only=True)
class UserDTO:
    first_name: str
    last_name: str
    username: str
    password: str
    email: str
    organization: Organizations
    is_active: bool
    is_admin: bool
    is_superuser: bool
    role: Roles
    phone_number: str
    telegram: str
    description: str


@dataclass(kw_only=True)
class CreateUserDTO(UserDTO):
    """DTO для создания нового пользователя системы."""

    requester_username: str


@dataclass
class UpdateUserDTO:
    """DTO для обновления существующего пользователя системы."""

    requester_username: str
    subject_username: str

    first_name: str | None = None
    last_name: str | None = None
    username: str | None = None
    email: str | None = None
    organization: Organizations | None = None
    is_active: bool | None = None
    is_admin: bool | None = None
    is_superuser: bool | None = None
    role: Roles | None = None
    phone_number: str | None = None
    telegram: str | None = None
    description: str | None = None


@dataclass
class ChangeUserPasswordDTO:
    """DTO для изменения пароля существующего пользователя системы."""

    old_password: str
    new_password: str
