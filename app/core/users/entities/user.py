from dataclasses import InitVar, dataclass

from core.enums import (
    EntityIdRange,
    Organizations,
    Roles,
)
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
    check_set_password,
)
from core.users.exceptions import (
    DomainValidationException,
    INVALID_DESCRIPTION_EXCEPTION_TEXT,
    ForbiddenCreate,
)
from core.utils import hash_password


@dataclass(frozen=True, slots=True, kw_only=True)
class UserEntity:
    def __eq__(self, other):
        if not isinstance(other, UserEntity):
            return NotImplemented
        return self.username == other.username

    id: int | None
    first_name: str
    last_name: str
    username: str
    organization: Organizations
    email: str
    password: bytes
    is_active: bool
    is_admin: bool
    is_superuser: bool
    role: Roles
    phone_number: str = ''
    telegram: str = ''
    description: str = ''
    full_validate: InitVar[bool] = True

    def __post_init__(self, full_validate):
        if not full_validate:
            return
        if self.id is not None and not check_field_id_is_valid(self.id):
            raise DomainValidationException(
                f'Недопустимый id пользователя: {self.id!r}. '
                f'Должен быть в диапазоне {EntityIdRange.MIN_ID}...{EntityIdRange.MAX_ID}'
            )
        if not check_email_is_valid(self.email):
            raise DomainValidationException(
                f'Недопустимый email пользователя: {self.email!r}.'
            )
        if not check_firstname_is_valid(self.first_name):
            raise DomainValidationException(
                f'Недопустимый first_name пользователя: {self.first_name!r}.'
            )
        if not check_lastname_is_valid(self.last_name):
            raise DomainValidationException(
                f'Недопустимый last_name пользователя: {self.last_name!r}.'
            )
        if not check_username_is_valid(self.username):
            raise DomainValidationException(
                f'Недопустимый username пользователя: {self.username!r}.'
            )
        check_is_valid_enum(Organizations, self.organization)
        if not check_password_is_valid(self.password):
            raise DomainValidationException(f'Недопустимый password пользователя.')
        if not isinstance(self.is_active, bool):
            raise DomainValidationException(
                f'Значение "is_active" должно быть типа bool.'
            )
        if not isinstance(self.is_admin, bool):
            raise DomainValidationException(
                f'Значение "is_admin" должно быть типа bool.'
            )
        if not isinstance(self.is_superuser, bool):
            raise DomainValidationException(
                f'Значение "is_superuser" должно быть типа bool.'
            )
        check_is_valid_enum(Roles, self.role)
        if not check_phone_number_is_valid(self.phone_number):
            raise DomainValidationException(
                f'Недопустимый phone_number пользователя: {self.phone_number!r}.'
            )
        if not check_telegram_is_valid(self.telegram):
            raise DomainValidationException(
                f'Недопустимый telegram пользователя: {self.telegram!r}. Должен начинаться с @'
            )
        if not check_description_is_valid(self.description):
            raise DomainValidationException(INVALID_DESCRIPTION_EXCEPTION_TEXT)

    def allow_to_crete_new_user(self) -> bool:
        return self.is_active and self.is_superuser


@dataclass(frozen=True, slots=True, kw_only=True)
class CreateNewUserEntity:
    first_name: str
    last_name: str
    username: str
    organization: Organizations
    email: str
    password: str
    is_active: bool
    is_admin: bool
    is_superuser: bool
    role: Roles
    phone_number: str = ''
    telegram: str = ''
    description: str = ''

    def __post_init__(self):
        # Validate only password in this point.
        # Extra validation in UserEntity instance.
        if not check_set_password(self.password):
            raise DomainValidationException(f'Недопустимый формат пароля.')
        return UserEntity(
            id=None,
            first_name=self.first_name,
            last_name=self.last_name,
            username=self.username,
            organization=self.organization,
            email=self.email,
            password=hash_password(self.password),
            is_active=self.is_active,
            is_admin=self.is_admin,
            is_superuser=self.is_superuser,
            role=Roles(self.role),
            phone_number=self.phone_number,
            telegram=self.telegram,
            description=self.description,
        )


if __name__ == '__main__':
    try:
        user = UserEntity(
            id=321,
            first_name='Chook',
            last_name='Gekk',
            username='chokk',
            organization=Organizations.SDP,
            email='example@example.com',
            password=b'mysecret',
            is_active=True,
            is_admin=True,
            is_superuser=True,
            role=Roles.superuser,
            phone_number='',
            telegram='',
            description='',
        )
    except DomainValidationException as e:
        print(f'e: {e}')

    user2 = CreateNewUserEntity(
        first_name='Chookaaa',
        last_name='Gekk',
        username='chokk',
        organization=Organizations.SDP,
        email='example@example.com',
        password='sadf',
        is_active=True,
        is_admin=True,
        is_superuser=True,
        role=Roles.superuser,
        phone_number='',
        telegram='',
        description='',
    )

    print(user2)
