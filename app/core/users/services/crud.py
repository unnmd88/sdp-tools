from collections.abc import Sequence

from application.dtos.users import CreateUserDTO, UpdateUserDTO
from application.interfaces.cache.users import UsersCacheProtocol
from application.interfaces.repositories.users import UsersRepositoryProtocol
from core.enums import Organizations, Roles
from core.field_validators import check_set_password
from core.users.entities.user import UserEntity
from core.users.exceptions import (
    UserNotFoundByIdException,
    UserNotFoundByUsernameException,
    InvalidPasswordToSet,
    UserAlreadyExistsException,
    ForbiddenCreate,
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
        print(f'requestor_entity={requestor_entity}')
        if requestor_entity is None or not requestor_entity.allow_to_crete_new_user():
            raise ForbiddenCreate
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

    async def update_user(self, user: UpdateUserDTO) -> UserEntity: ...
