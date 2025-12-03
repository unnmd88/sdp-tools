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
    check_username_is_valid, check_telegram_is_valid,
)
from core.mixins.id import IdMixin
from core.users.exceptions import DomainValidationException, INVALID_DESCRIPTION_EXCEPTION_TEXT


@dataclass(frozen=True, slots=True, kw_only=True)
class UserEntity:
    id: int
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
        if not check_field_id_is_valid(self.id):
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
            raise DomainValidationException(
                f'Недопустимый password пользователя.'
            )
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


    # print(user)
