from dataclasses import dataclass, InitVar

from app.core.enums.organizations import Organizations
from app.core.enums.roles import Roles
from core.enums.entity import EntityIdRange
from core.field_validators import check_field_id_is_valid, check_field_email_is_valid, check_firstname_is_valid, \
    check_lastname_is_valid, check_username_is_valid, check_password_is_valid, check_is_valid_enum
from core.users.exceptions import DomainValidationException


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
                detail=(
                    f'Недопустимый id пользователя: {self.id!r}. '
                    f'Должен быть в диапазоне {EntityIdRange.MIN_ID}...{EntityIdRange.MAX_ID}'
                )
            )
        if not check_field_email_is_valid(self.email):
            raise DomainValidationException(
                detail=f'Недопустимый email пользователя: {self.email!r}.'
            )
        if not check_firstname_is_valid(self.first_name):
            raise DomainValidationException(
                detail=f'Недопустимый first_name пользователя: {self.first_name!r}.'
            )
        if not check_lastname_is_valid(self.last_name):
            raise DomainValidationException(
                detail=f'Недопустимый last_name пользователя: {self.last_name!r}.'
            )
        if not check_username_is_valid(self.username):
            raise DomainValidationException(
                detail=f'Недопустимый username пользователя: {self.username!r}.'
            )
        check_is_valid_enum(Organizations, self.organization)
        if not check_password_is_valid(self.password):
            raise DomainValidationException(
                detail=f'Недопустимый password пользователя.'
            )
        if not isinstance(self.is_active, bool):
            raise DomainValidationException(
                detail=f'Значение "is_active" должно быть типа bool.'
            )
        if not isinstance(self.is_admin, bool):
            raise DomainValidationException(
                detail=f'Значение "is_admin" должно быть типа bool.'
            )
        if not isinstance(self.is_superuser, bool):
            raise DomainValidationException(
                detail=f'Значение "is_superuser" должно быть типа bool.'
            )
        check_is_valid_enum(Roles, self.role)

        #TO DO phone_number telegram description







    def validate_types(self):
        # Check types
        if not isinstance(self.id, int):
            raise TypeError(f'id must be an {int!r}')
        if not isinstance(self.first_name, str):
            raise TypeError(f'first_name must be an {str!r}')
        if not isinstance(self.last_name, str):
            raise TypeError(f'last_name must be an {str!r}')
        if not isinstance(self.username, str):
            raise TypeError(f'username must be an {str!r}')
        try:
            Organizations(self.first_name)
        except ValueError:
            raise TypeError(f'organization id must be an {Organizations!r}')
        if not isinstance(self.email, str):
            raise TypeError(f'email must be an {str!r}')
        if not isinstance(self.password, str):
            raise TypeError(f'password must be an {bytes!r}')
        if not isinstance(self.is_active, bool):
            raise TypeError(f'is_active must be an {bool!r}')
        if not isinstance(self.is_admin, bool):
            raise TypeError(f'is_admin must be an {bool!r}')
        if not isinstance(self.is_superuser, bool):
            raise TypeError(f'is_superuser must be an {bool!r}')
        try:
            Roles(self.role)
        except ValueError:
            raise TypeError(f'organization id must be an {Roles!r}')
        if not isinstance(self.phone_number, str):
            raise TypeError(f'phone_number must be an {str!r}')
        if not isinstance(self.telegram, str):
            raise TypeError(f'telegram must be an {str!r}')
        if not isinstance(self.description, str):
            raise TypeError(f'description must be an {str!r}')


if __name__ == '__main__':
    user = UserEntity(
        id=321,
        first_name='Chook',
        last_name='Gekk',
        username='chokky',
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
    print(user)