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
class UpdateUserDTO(UserDTO):
    """DTO для создания обновления существующего пользователя системы."""


@dataclass
class ChangeUserPasswordDTO:
    """DTO для изменения пароля существующего пользователя системы."""

    old_password: str
    new_password: str
