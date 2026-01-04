from dataclasses import dataclass, field

from core.enums import Roles, Organizations


@dataclass(slots=True, frozen=True, kw_only=True)
class SearchUsersDTO:
    """ DTO для поиска сущности в хранилище. """

    customer: str


@dataclass(slots=True, frozen=True, kw_only=True)
class SearchUserDTO(SearchUsersDTO):
    """ DTO для поиска сущности в хранилище. """

    subject: str



@dataclass(kw_only=True)
class UserDTO:
    first_name: str
    last_name: str
    username: str
    password: str
    email: str
    organization: Organizations
    is_active: bool
    role: Roles
    phone_number: str
    telegram: str
    description: str


@dataclass(kw_only=True)
class CreateUserDTO(UserDTO):
    """DTO для создания нового пользователя системы."""

    customer: str


@dataclass(slots=True, frozen=True, kw_only=True)
class ChangeUserPasswordDTO(SearchUserDTO):
    """DTO для изменения пароля существующего пользователя системы."""

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



