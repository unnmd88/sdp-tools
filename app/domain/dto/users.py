from dataclasses import dataclass, field

from domain.enums.unsorted import Roles, Organizations


@dataclass(slots=True, frozen=True, kw_only=True)
class SearchUsersDTO:
    """DTO для поиска сущности в хранилище."""

    customer: str


@dataclass(slots=True, frozen=True, kw_only=True)
class GetUserFromRepoDTO:
    """DTO для поиска сущности в хранилище."""

    subject: str
    raise_if_not_found: bool
    raise_if_not_active: bool


@dataclass(slots=True, frozen=True, kw_only=True)
class UserDTO:
    firstname: str | None
    lastname: str | None
    username: str
    password: str | bytes = field(repr=False)
    email: str | None
    organization: Organizations
    is_active: bool
    role: Roles
    phone_number: str | None
    telegram: str | None
    description: str


@dataclass(slots=True, frozen=True, kw_only=True)
class CreateUserDTO(UserDTO):
    """DTO для создания нового пользователя системы."""

    customer: str


@dataclass(slots=True, frozen=True, kw_only=True)
class ChangeUserPasswordDTO:
    """DTO для изменения пароля существующего пользователя системы."""

    subject: str
    old_password: str = field(repr=False)
    new_password: str = field(repr=False)


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
