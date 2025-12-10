from collections.abc import Sequence
from dataclasses import asdict

from application.interfaces.cache.users import UsersCacheProtocol
from application.interfaces.repositories.users import UsersRepositoryProtocol
from core.dto.users import CreateUserDTO, UpdateUserDTO
from core.enums import Organizations, Roles, Permission
from core.exceptions.base import CreateError, UpdateError
from core.field_validators import check_set_password
from core.security_policies.services.user_permissions import check_permission_to_update_entity
from core.users.entities.user import UserEntity
from core.users.exceptions import (
    UserNotFoundByIdException,
    UserNotFoundByUsernameException,
    InvalidPasswordToSet,
    UserAlreadyExistsException,
    ForbiddenCreate, ForbiddenUpdate,
)
from core.utils import hash_password


class UsersServiceImpl:
    def __init__(
        self,
        repository: UsersRepositoryProtocol,
        cache: UsersCacheProtocol = None,  # TO DO
    ):
        self.repository = repository
        self.cache = cache

    async def get_user_by_username_or_none(self, username: str) -> UserEntity:
        if (
            user := await self.repository.get_user_by_username_or_none(username)
        ) is None:
            raise UserNotFoundByUsernameException(username)
        return user

    async def get_user_by_id_or_none(self, user_id: int) -> UserEntity:
        if self.cache and (user := await self.cache.get_by_id(user_id)):
            return user
        if (user := await self.repository.get_one_by_id_or_none(user_id)) is None:
            raise UserNotFoundByIdException(user_id)
        return user

    async def get_all_users(self) -> Sequence[UserEntity]:
        return await self.repository.get_all()

    async def create_user(self, data: CreateUserDTO) -> UserEntity:
        requestor_entity: UserEntity = (
            await self.repository.get_user_by_username_or_none(data.requester_username)
        )
        if requestor_entity is None:
            raise ForbiddenCreate
        requestor_entity.check_permissions(Permission.CREATE_USERS)
        if not check_set_password(data.password):
            raise InvalidPasswordToSet
        if requestor_entity.username == data.username:
            raise UserAlreadyExistsException(data.username)
        user_already_exists = await self.repository.get_user_by_username_or_none(
            data.username
        )
        if user_already_exists:
            raise UserAlreadyExistsException(data.username)
        entity = UserEntity(
            id=None,
            first_name=data.first_name,
            last_name=data.last_name,
            username=data.username,
            password=hash_password(data.password),
            email=data.email,
            organization=Organizations(data.organization),
            is_active=data.is_active,
            is_admin=data.is_admin,
            is_superuser=data.is_superuser,
            role=Roles(data.role),
            phone_number=data.phone_number,
            telegram=data.telegram,
            description=data.description,
        )
        return await self.repository.add(entity)

    async def update_user(self, data: UpdateUserDTO) -> UserEntity:
        requestor_entity: UserEntity = (
            await self.repository.get_user_by_username_or_none(data.requester_username)
        )
        if requestor_entity.username != data.subject_username:
            to_update_entity = await self.repository.get_user_by_username_or_none(data.subject_username)
            if to_update_entity is None:
                raise CreateError('Пользователь не найден в базе')
        else:
            to_update_entity = requestor_entity
        check_permission_to_update_entity(
            requestor_entity=requestor_entity,
            to_update_entity=to_update_entity,
            data=data
        )
        if data.password:
            raise ForbiddenUpdate('Изменение пароля запрещено.')
        to_update_entity_as_dict = asdict(to_update_entity)
        data_as_dict = asdict(data)
        for k, v in data_as_dict.items():
            if k not in to_update_entity_as_dict:
                raise UpdateError(f'Некорректное поле для изменения: {k!r}')
            if k is not None:
                to_update_entity_as_dict[k] = v
        UserEntity(**to_update_entity_as_dict) # Проверка, что данные для обновления валидны
        return await self.repository.update(**data_as_dict)