from datetime import datetime
from typing import Any

from core.base_entity import AbstractEntity
from core.contracts import contract
from core.enums import (
    Organizations,
    Roles,
    Permissions,
)
from core.exceptions.contract import (
    ContractViolationBusinessRulesError,
    ContractViolationInvariantError,
)

from core.users.entities.permissions import UserPermissions
from core.users.requires import (
    username_pre_requires,
    firstname_pre_requires,
    lastname_pre_requires,
)
from core.users.rules_messages import BusinessRulesViolationsMessages
from core.users.services.role_permissions import get_role_permissions
from core.users.services.user_password import validate_password


# @dataclass(frozen=True, slots=True, kw_only=True)
# class UserEntity(BaseEntityMixin):
#     first_name: str | None
#     last_name: str | None
#     username: str
#     organization: Organizations
#     email: str | None
#     password: bytes = field(repr=False)
#     is_active: bool
#     role: Roles
#     phone_number: str | None
#     telegram: str | None
#     description: str
#     permissions: UserPermissions = field(default_factory=UserPermissions)
#     full_validate: InitVar[bool] = True
#
#     def __post_init__(
#         self,
#         full_validate,
#     ):
#         if not full_validate:
#             return
#         if self.id is not None and not check_field_id_is_valid(self.id):
#             raise DomainValidationError(
#                 f'Недопустимый id пользователя: {self.id!r}. '
#                 f'Должен быть в диапазоне {EntityIdRange.MIN_ID}...{EntityIdRange.MAX_ID}'
#             )
#         if not check_email_is_valid(self.email):
#             raise DomainValidationError(
#                 f'Недопустимый email пользователя: {self.email!r}.'
#             )
#         if not check_firstname_is_valid(self.first_name):
#             raise DomainValidationError(
#                 f'Недопустимый first_name пользователя: {self.first_name!r}.'
#             )
#         if not check_lastname_is_valid(self.last_name):
#             raise DomainValidationError(
#                 f'Недопустимый last_name пользователя: {self.last_name!r}.'
#             )
#         if not check_username_is_valid(self.username):
#             raise DomainValidationError(
#                 f'Недопустимый username пользователя: {self.username!r}.'
#             )
#         check_is_valid_enum(Organizations, self.organization)
#         if not check_password_is_valid(self.password):
#             raise DomainValidationError(f'Недопустимый password пользователя.')
#         if not isinstance(self.is_active, bool):
#             raise DomainValidationError(f'Значение "is_active" должно быть типа bool.')
#         check_is_valid_enum(Roles, self.role)
#         if not check_phone_number_is_valid(self.phone_number):
#             raise DomainValidationError(
#                 f'Недопустимый phone_number пользователя: {self.phone_number!r}.'
#             )
#         if not check_telegram_is_valid(self.telegram):
#             raise DomainValidationError(
#                 f'Недопустимый telegram пользователя: {self.telegram!r}. Должен начинаться с @'
#             )
#         if not check_description_is_valid(self.description):
#             raise DomainValidationError(INVALID_DESCRIPTION_EXCEPTION_TEXT)
#         self._set_permissions()
#
#     def __eq__(self, other):
#         if not isinstance(other, UserEntity):
#             raise NotImplementedError
#         return self.username == other.username
#
#     def _set_permissions(self):
#         if not self.is_active:
#             self.permissions.revoke_all()
#             return
#         if self.role == Roles.superuser:
#             self.permissions.add_all_user_permissions()
#         elif self.role == Roles.admin:
#             self.permissions.add_all_user_permissions(
#                 exclude={Permissions.CREATE_USERS, Permissions.UPDATE_USERS}
#             )
#
#     def validate_password(self, password: str) -> bool:
#         return validate_password(
#             password=password,
#             hashed_password=self.password,
#         )
#
#     @property
#     def is_superuser(self) -> bool:
#         return self.role == Roles.superuser


class UserEntity(AbstractEntity):
    def __init__(
        self,
        id: int,
        username: str,
        firstname: str | None,
        lastname: str | None,
        organization: Organizations,
        email: str | None,
        password: bytes,
        is_active: bool,
        role: Roles,
        phone_number: str | None,
        telegram: str | None,
        description: str,
        created_at: datetime | None,
        updated_at: datetime | None,
    ):
        super().__init__(id=id, created_at=created_at, updated_at=updated_at)
        self._username = self.set_username(username)
        self._firstname = self.set_firstname(firstname)
        self._lastname = self.set_lastname(lastname)
        self._organization = organization
        self._email = email
        self._password = password
        self._is_active = is_active
        self._role = role
        self._phone_number = phone_number
        self._telegram = telegram
        self._description = description
        self._permissions = get_role_permissions(self._role)
        self.invariant_names()
        self.invariant_password()

    def __eq__(self, other):
        if isinstance(other, UserEntity):
            return self._username == other.username
        raise NotImplementedError

    def __repr__(self):
        return (
            f'{self.__class__.__name__}('
            f'id={self._id!r} '
            f'username={self.username!r} '
            f'built_at={self.built_at.strftime(self.time_format)!r}'
            f')'
        )

    def to_dict(self) -> dict:
        return {
            'id': self._id,
            'username': self._username,
            'firstname': self._firstname,
            'lastname': self._lastname,
            'created_at': self._created_at.strftime(self.time_format) if self._created_at is not None else None,
            'updated_at': self._updated_at.strftime(self.time_format) if self._updated_at is not None else None,
            'built_at': self._built_at.strftime(self.time_format),
        }

    @property
    def username(self) -> str:
        return self._username

    @property
    def firstname(self) -> str | None:
        return self._firstname

    @property
    def lastname(self) -> str | None:
        return self._lastname

    @property
    def organization(self) -> Organizations:
        return self._organization

    @property
    def email(self) -> str | None:
        return self._email

    @property
    def password(self) -> bytes:
        return self._password

    @property
    def is_active(self) -> bool:
        return self._is_active

    @property
    def role(self) -> Roles:
        return self._role

    @property
    def phone_number(self) -> str | None:
        return self._phone_number

    @property
    def telegram(self) -> str | None:
        return self._telegram

    @property
    def description(self) -> str:
        return self._description

    def has_permission(self, permission: Permissions) -> bool:
        return permission in self._permissions

    def set_username(self, username: str) -> str:
        username = self._validate_username(username, _locals=locals())
        self._username = username
        return self._username

    def set_firstname(self, firstname: str | None) -> str | None:
        if firstname is None:
            self._firstname = None
            return self._firstname
        firstname = self._validate_first_name(firstname, _locals=locals())
        self._firstname = firstname
        return self._firstname

    def set_lastname(self, lastname: str | None) -> str | None:
        if lastname is None:
            self._lastname = None
            return self._lastname
        lastname = self._validate_last_name(lastname, _locals=locals())
        self._lastname = lastname
        return self._lastname

    def validate_password(self, password: str) -> bool:
        return validate_password(password, self._password)

    @contract(
        preconditions=username_pre_requires,
        # postconditions=username_post_requires if not os.environ.get("PROD") else None,
    )
    def _validate_username(
        self,
        username: str,
        _locals: dict[str, Any] = None,
    ) -> str:
        return username

    @contract(preconditions=firstname_pre_requires)
    def _validate_first_name(
        self,
        first_name: str,
        _locals: dict[str, Any] = None,
    ) -> str:
        return first_name

    @contract(preconditions=lastname_pre_requires)
    def _validate_last_name(self, lastname: str) -> str:
        return lastname

    def invariant_names(self):
        if self._username == self._lastname:
            raise ContractViolationBusinessRulesError(
                BusinessRulesViolationsMessages.username_and_lastname_must_be_different
            )
        if self._username == self._firstname:
            raise ContractViolationBusinessRulesError(
                BusinessRulesViolationsMessages.username_and_firstname_must_be_different
            )

    def invariant_password(self) -> None:
        if self._password is None:
            # TODO: Обязательно добавить логирование!!
            raise ContractViolationInvariantError('Пароль не может быть пустым')
        if not isinstance(self._password, bytes):
            # TODO: Обязательно добавить логирование!!
            raise ContractViolationInvariantError('Пароль должен быть типа bytes')

    def invariant_permissions(self) -> None:
        if not self._is_active and self._permissions:
            raise ContractViolationInvariantError(
                f'У пользователя с username: {self._username!r} не должно быть разрешений, т.к. он не активен.'
            )
        # TODO: добавить проверку на наполнение разрешений в зависимости от роли.

    def _init_permissions(self):
        if not self.is_active:
            self._permissions.revoke_all()
            return
        if self.role == Roles.superuser:
            self._permissions.add_all_user_permissions()
        elif self.role == Roles.admin:
            self._permissions.add_all_user_permissions(
                exclude={Permissions.CREATE_USERS, Permissions.UPDATE_USERS}
            )


if __name__ == '__main__':
    pass
    # user = UserEntity(
    #     id=1,
    #     firstname='Junkers',
    #     lastname=None,
    #     username='Junker',
    #     created_at=datetime.now(),
    #     updated_at=None,
    # )
    # print(user)
    # print(user.to_dict())
    # print(user.to_json())
