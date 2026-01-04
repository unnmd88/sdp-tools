from dataclasses import InitVar, dataclass, field

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
from core.users.exceptions import (
    DomainValidationError,
    INVALID_DESCRIPTION_EXCEPTION_TEXT,
    InvalidUsernameOrPasswordError,
)
from core.security_policies.permissions import UserPermissions
from core.security_policies.user_password import validate_password


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


class UserAccessControl:

    def __init__(self, user_entity: UserEntity = None):
        self._user_entity = user_entity

    def load_user_entity(self, user_entity: UserEntity) -> None:
        self._user_entity = user_entity

    def updating_another_user(
        self,
        subject_username: str
    ) -> None:
        if self._user_entity.username == subject_username:
            return None
        if not self._user_entity.permissions.has(Permissions.UPDATE_USERS):
            raise UserPermissionsError('обновления другого пользователя')
        return None

    def read_user(self, readable_username_or_id: str | int) -> None:
        if (
            self._user_entity.username == readable_username_or_id
            or self._user_entity.id == readable_username_or_id
            or self._user_entity.permissions.has(Permissions.READ_USERS)
        ):
            return None
        raise UserPermissionsError('чтения другого пользователя')

    def read_any_user(self) -> None:
        if not self._user_entity.permissions.has(Permissions.READ_USERS):
            raise UserPermissionsError('чтения другого пользователя')

    def create_user(self) -> None:
        if not self._user_entity.permissions.has(Permissions.CREATE_USERS):
            raise UserPermissionsError('создания нового пользователя')

    def change_password_for_any_user(self) -> None:
        if not self._user_entity.permissions.has(Permissions.UPDATE_USERS):
            raise UserPermissionsError('изменения другого пользователя')

    def validate_password(self, password: str):
        if not validate_password(
            password=password,
            hashed_password=self._user_entity.password,
        ):
            raise InvalidUsernameOrPasswordError

    # def access_control(self, *permissions: Permissions):
    #     """
    #     Проверка наличия permissions для пользователя. В случае, если один хотя бы одно из permissions
    #     отсутствует - будет выброшено исключение.
    #     :param permissions: Разрешения пользователя, подлежащие проверки на наличие.
    #     :raises UserPermissionsError: Исключение, если хотя бы одно из permissions отсутствует.
    #     :return: None.
    #     """
    #     if not (permissions := set(permissions)):
    #         raise ValueError('permissions cant be empty.')
    #     if not permissions.issubset(self._user_entity.permissions.get_all()):
    #         raise ValueError('Bad members in permissions.')
    #     difference = self._user_entity.permissions.has_difference(permissions)
    #     if difference:
    #         raise UserPermissionsError(f'Отсутствуют права: {",".join(difference)}')

    def read_regions(self):
        if not self._user_entity.permissions.has(Permissions.READ_REGIONS):
            raise UserPermissionsError(Permissions.READ_REGIONS)

    def read_passport_group(self):
        if not self._user_entity.permissions.has(Permissions.READ_PASSPORT_GROUPS):
            raise UserPermissionsError(Permissions.READ_PASSPORT_GROUPS)


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
        role=Roles.superuser,
        phone_number='',
        telegram='',
        description='',
    )




