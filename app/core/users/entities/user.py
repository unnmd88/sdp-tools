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
from core.mixins import BaseEntityMixin
from core.users.exceptions import (
    DomainValidationError,
    INVALID_DESCRIPTION_EXCEPTION_TEXT,
    UserPermissionsError, InvalidUsernameOrPasswordError, InactiveUserError,
)
from core.users.value_objects.permissions import UserPermissions
from core.utils import hash_password, validate_password


@dataclass(frozen=True, slots=True, kw_only=True)
class UserEntity(BaseEntityMixin):

    first_name: str
    last_name: str
    username: str
    organization: Organizations
    email: str
    password: bytes = field(repr=False)
    is_active: bool
    role: Roles
    phone_number: str
    telegram: str
    description: str
    permissions: UserPermissions = field(default_factory=UserPermissions)
    raise_if_not_active: InitVar[bool] = True
    full_validate: InitVar[bool] = True

    def __post_init__(self, raise_if_not_active, full_validate,):
        if raise_if_not_active and not self.is_active:
            raise DomainValidationError(f'Пользователь с id={self.id} username={self.username!r} не активен.')
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
            return NotImplementedError
        return self.username == other.username

    def validate_password(self, password: str):
        if not validate_password(
            password=password,
            hashed_password=self.password,
        ):
            raise InvalidUsernameOrPasswordError

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

    def check_has_permission_to_crete_new_user(self) -> None:
        if self.role == Roles.superuser:
            return None
        raise UserPermissionsError(self.username)

    def has_permissions(self, *permissions: Permissions):
        """
        Проверка наличия permissions для пользователя. В случае, если один хотя бы одно из permissions
        отсутствует - будет выброшено исключение.
        :param permissions: Разрешения пользователя, подлежащие проверки на наличие.
        :raises UserPermissionsError: Исключение, если хотя бы одно из permissions отсутствует.
        :return: None.
        """
        if not permissions:
            raise TypeError('permissions cant be empty.')
        all_permissions = self.permissions.get_all()
        if not all(Permissions(p) in all_permissions for p in permissions):
            raise UserPermissionsError(f'Отсутствуют права: {",".join(p for p in permissions if p not in all_permissions)}')

    def check_permission_read_region(self):
        self.has_permissions(Permissions.READ_REGIONS)

    def check_permission_read_passport_groups(self):
        self.has_permissions(Permissions.READ_PASSPORT_GROUPS)

    def check_permission_read_tlo(self):
        self.has_permissions(Permissions.READ_TLO)

    def check_permission_to_search_any_user(self) -> None:
        if self.role in (Roles.admin, Roles.superuser):
            return None
        raise UserPermissionsError(self.username)



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
    user = UserEntity(
        id=321,
        first_name='Chook',
        last_name='Gekk',
        username='chokk',
        organization=Organizations.SDP,
        email='example@example.com',
        password=b'mysecret',
        is_active=False,
        is_admin=True,
        is_superuser=True,
        role=Roles.superuser,
        phone_number='',
        telegram='',
        description='',
        raise_if_not_active=False,
        # full_validate=False,
    )



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
