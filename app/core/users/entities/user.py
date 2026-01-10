from dataclasses import InitVar, dataclass, field
from datetime import datetime
from enum import StrEnum

from core.base_entity import BaseEntity
from core.enums import (
    EntityIdRange,
    Organizations,
    Roles, Permissions,
)
from core.exceptions.base import UserPermissionsError
from core.field_validators import (
    check_description_is_valid,
    check_email_is_valid,
    check_field_id_is_valid,
    check_firstname_is_valid,
    check_is_valid_enum,
    check_lastname_is_valid,
    check_password_is_valid,
    check_phone_number_is_valid,
    check_username_is_valid,
    check_telegram_is_valid,
)
from core.mixins import BaseEntityMixin
from core.services.contract import contract, ContractConditions
from core.services.field_validators import username_validator, first_name_or_lastname_validator
from core.users.exceptions import (
    DomainValidationError,
    INVALID_DESCRIPTION_EXCEPTION_TEXT,
)
from core.users.entities.permissions import UserPermissions
from core.users.services.user_password import validate_password


@dataclass(frozen=True, slots=True, kw_only=True)
class UserEntity(BaseEntityMixin):

    first_name: str | None
    last_name: str | None
    username: str
    organization: Organizations
    email: str | None
    password: bytes = field(repr=False)
    is_active: bool
    role: Roles
    phone_number: str | None
    telegram: str | None
    description: str
    permissions: UserPermissions = field(default_factory=UserPermissions)
    full_validate: InitVar[bool] = True

    def __post_init__(self, full_validate,):

        if not full_validate:
            return
        if self.id is not None and not check_field_id_is_valid(self.id):
            raise DomainValidationError(
                f'Недопустимый id пользователя: {self.id!r}. '
                f'Должен быть в диапазоне {EntityIdRange.MIN_ID}...{EntityIdRange.MAX_ID}'
            )
        if not check_email_is_valid(self.email):
            raise DomainValidationError(
                f'Недопустимый email пользователя: {self.email!r}.'
            )
        if not check_firstname_is_valid(self.first_name):
            raise DomainValidationError(
                f'Недопустимый first_name пользователя: {self.first_name!r}.'
            )
        if not check_lastname_is_valid(self.last_name):
            raise DomainValidationError(
                f'Недопустимый last_name пользователя: {self.last_name!r}.'
            )
        if not check_username_is_valid(self.username):
            raise DomainValidationError(
                f'Недопустимый username пользователя: {self.username!r}.'
            )
        check_is_valid_enum(Organizations, self.organization)
        if not check_password_is_valid(self.password):
            raise DomainValidationError(f'Недопустимый password пользователя.')
        if not isinstance(self.is_active, bool):
            raise DomainValidationError(
                f'Значение "is_active" должно быть типа bool.'
            )
        check_is_valid_enum(Roles, self.role)
        if not check_phone_number_is_valid(self.phone_number):
            raise DomainValidationError(
                f'Недопустимый phone_number пользователя: {self.phone_number!r}.'
            )
        if not check_telegram_is_valid(self.telegram):
            raise DomainValidationError(
                f'Недопустимый telegram пользователя: {self.telegram!r}. Должен начинаться с @'
            )
        if not check_description_is_valid(self.description):
            raise DomainValidationError(INVALID_DESCRIPTION_EXCEPTION_TEXT)
        self._set_permissions()


    def __eq__(self, other):
        if not isinstance(other, UserEntity):
            raise NotImplementedError
        return self.username == other.username

    def _set_permissions(self):
        if not self.is_active:
            self.permissions.revoke_all()
            return
        if self.role == Roles.superuser:
            self.permissions.add_all_user_permissions()
        elif self.role == Roles.admin:
            self.permissions.add_all_user_permissions(
                exclude={Permissions.CREATE_USERS, Permissions.UPDATE_USERS}
            )

    def validate_password(self, password: str) -> bool:
        return validate_password(
            password=password,
            hashed_password=self.password,
        )

    @property
    def is_superuser(self) -> bool:
        return self.role == Roles.superuser



class RulesViolationsMessages(StrEnum):
    username = "username должен быть от 2 до 32 символов длиной и содержать только буквы латинского алфавита и цифры."
    first_name = "first_name должен быть строкой и содержать только буквы латинского алфавита."
    last_name = "last_name должен быть строкой и содержать только буквы латинского алфавита."


class UserEntity(BaseEntity):
    def __init__(
        self,
        entity_id: int | None,
        username: str,
        first_name: str | None,
        last_name: str | None,
        created_at: datetime | None,
        updated_at: datetime | None,

    ):
        super().__init__(entity_id=entity_id, created_at=created_at, updated_at=updated_at)
        self._username = self._validate_username(username)
        self._firstname = self._validate_first_name(first_name)
        self._lastname = self._validate_last_name(last_name)

    def __eq__(self, other):
        if isinstance(other, UserEntity):
            return self._username == other.username
        raise NotImplementedError

    def __repr__(self):
        return (
            f'{self.__class__.__name__}('
            f'id={self.entity_id!r} '
            f'username={self.username!r} '
            f'built_at={self.built_at.strftime("%d-%m-%Y, %H:%M:%S")!r}'
            f')'
        )

    @property
    def username(self) -> str:
        return self._username

    @username.setter
    def username(self, username: str):
        self._username = self._validate_username(username)
        if self._username == self._lastname:
            raise DomainValidationError("username не должен совпадать с last_name")
        if self._username == self._firstname:
            raise DomainValidationError("username не должен совпадать с firstname")

    @property
    def firstname(self) -> str | None:
        return self._firstname

    @firstname.setter
    def firstname(self, first_name: str | None):
        if first_name is not None:
            self._firstname = self._validate_first_name(first_name)
            if self._firstname == self._lastname:
                raise DomainValidationError("first_name не должен совпадать с last_name")
            if self._firstname == self._username:
                raise DomainValidationError("first_name не должен совпадать с username")
        else:
            self._firstname = None

    @property
    def lastname(self) -> str | None:
        return self._lastname

    @lastname.setter
    def lastname(self, last_name: str | None):
        if last_name is not None:
            self._lastname = self._validate_last_name(last_name)
            if self._lastname == self._firstname:
                raise DomainValidationError("last_name не должен совпадать с first_name")
            if self._lastname == self._username:
                raise DomainValidationError("last_name не должен совпадать с username")
        else:
            self._lastname = None

    @contract(
        type_check=str,
        preconditions=ContractConditions(
            requires=[(username_validator, str(RulesViolationsMessages.username))]
        ),
        field_name="username",
    )
    def _validate_username(self, username: str) -> str:
        assert isinstance(username, str), "username должен быть строкой"
        assert (2 < len(username) < 32), "username должен быть от 2 до 32 символов длиной"
        assert username.isalnum() and not username.isnumeric(), "username должен содержать только буквы латинского алфавита и цифры."
        return username

    @contract(
        type_check=str | None,
        preconditions=ContractConditions(
            requires=[(first_name_or_lastname_validator, str(RulesViolationsMessages.first_name))]
        ),
        field_name="first_name",
    )
    def _validate_first_name(self, first_name: str) -> str:
        assert isinstance(first_name, str), "first_name должен быть строкой"
        assert first_name.isalpha(), "first_name должен содержать только буквы латинского алфавита."
        return first_name

    @contract(
        type_check=str | None,
        preconditions=ContractConditions(
            requires=[(first_name_or_lastname_validator, str(RulesViolationsMessages.last_name))]
        ),
        field_name="last_name",
    )
    def _validate_last_name(self, last_name: str) -> str:
        assert isinstance(last_name, str), "last_name должен быть строкой"
        assert last_name.isalpha(), "last_name должен содержать только буквы латинского алфавита."
        return last_name




if __name__ == '__main__':
    user = UserEntity(
        entity_id=321,
        first_name='dasdsa',
        last_name='Gekk',
        username='333r',
        created_at=datetime.now(),
        updated_at=None,
    )
    print(user)
    user.username = ('Juker')
    print(f"user.username = {user.username}")
    print(user)
    user.firstname = None
    print(user)
    user.lastname = None
    user.lastname = 'Juker'





