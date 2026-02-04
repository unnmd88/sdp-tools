from dataclasses import dataclass, field
from datetime import datetime

from domain.entities.user import UserEntity
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
    """DTO для существующего пользователя системы."""

    id: int
    firstname: str | None
    lastname: str | None
    username: str
    email: str | None
    organization: Organizations
    is_active: bool
    role: Roles
    is_superuser: bool
    phone_number: str | None
    telegram: str | None
    description: str
    created_at: str | None
    updated_at: str | None
    built_at: str | datetime

    @classmethod
    def from_entity(cls, entity: UserEntity) -> "UserDTO":
        return cls(**entity.to_dict())


@dataclass(slots=True, frozen=True, kw_only=True)
class CreateUserDTO:
    """DTO для создания нового пользователя системы."""

    customer: str

    firstname: str | None
    lastname: str | None
    username: str
    email: str | None
    organization: Organizations
    is_active: bool
    role: Roles
    phone_number: str | None
    telegram: str | None
    description: str
    password: str | bytes = field(repr=False)


@dataclass(slots=True, frozen=True, kw_only=True)
class ChangeUserPasswordDTO:
    """DTO для изменения пароля существующего пользователя системы."""

    old_password: str = field(repr=False)
    new_password: str = field(repr=False)


@dataclass(slots=True, frozen=True, kw_only=True)
class ChangeUserPasswordByAdminDTO:
    """DTO для изменения пароля существующего пользователя системы."""

    customer_id: int
    subject_username: str


@dataclass(slots=True, frozen=True, kw_only=True)
class ChangedUserPasswordByAdminDTO:

    username: str
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

    # organization: Organizations | None = None
    # is_active: bool | None = None
    # is_admin: bool | None = None
    # is_superuser: bool | None = None
    # role: Roles | None = None
    phone_number: str | None = None
    telegram: str | None = None
    # description: str | None = None
