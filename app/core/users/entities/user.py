from dataclasses import InitVar, dataclass, field


from core.enums import (
    EntityIdRange,
    Organizations,
    Roles, Permissions,
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
    DomainValidationError,
    INVALID_DESCRIPTION_EXCEPTION_TEXT,
    UserPermissionsError,
)
from core.users.value_objects.permissions import UserPermissions
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
    permissions: UserPermissions = field(default_factory=UserPermissions)

    def __post_init__(self, full_validate):
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
        if not isinstance(self.is_admin, bool):
            raise DomainValidationError(
                f'Значение "is_admin" должно быть типа bool.'
            )
        if not isinstance(self.is_superuser, bool):
            raise DomainValidationError(
                f'Значение "is_superuser" должно быть типа bool.'
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

    def _set_permissions(self):
        if not self.is_active:
            self.permissions.revoke_all()
            return

        if self.is_superuser:
            self.permissions.add_all_user_permissions()
        elif self.is_admin:
            self.permissions.add_all_user_permissions(
                exclude={Permissions.CREATE_USERS, Permissions.UPDATE_USERS}
            )

    def allow_to_crete_new_user(self) -> bool:
        return self.is_active and self.is_superuser

    def check_permissions(self, *permissions: Permissions):
        if not permissions:
            raise TypeError('permissions cant be empty')
        all_permissions = self.permissions.get_all()
        if not all(Permissions(p) in all_permissions for p in permissions):
            raise UserPermissionsError(f'Отсутствуют права: {",".join(p for p in permissions if p not in all_permissions)}')

    def check_permission_read_region(self):
        self.check_permissions(Permissions.READ_REGIONS)

    def check_permission_read_passport_groups(self):
        self.check_permissions(Permissions.READ_PASSPORT_GROUPS)

    def check_permission_read_tlo(self):
        self.check_permissions(Permissions.READ_TLO)


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
            raise DomainValidationError(f'Недопустимый формат пароля.')
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
    except DomainValidationError as e:
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
