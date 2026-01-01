import logging
from collections.abc import Sequence
from dataclasses import asdict

from app_logging.dev.config import USERS_LOGGER
from application.interfaces.cache.users import UsersCacheProtocol
from application.interfaces.repositories.users import UsersRepositoryProtocol
from core.dto.common import FiltersForSearchDTO
from core.dto.users import CreateUserDTO, UpdateUserDTO, SearchUserByIdDTO, SearchUsersDTO
from core.enums import Organizations, Roles
from core.exceptions.base import CreateError, UpdateError
from core.field_validators import check_set_password
from core.security_policies.exceptions import InactiveUserError
from core.security_policies.services.user_permissions import check_permission_to_update_entity
from core.users.entities.user import UserEntity
from core.users.exceptions import (
    UserNotFoundByIdError,
    UserNotFoundByUsernameError,
    InvalidUserPasswordToSetError,
    UserAlreadyExistsError,
    ForbiddenUpdateError, UserPermissionsError,
)
from core.utils import hash_password


logger = logging.getLogger(USERS_LOGGER)


class UsersServiceImpl:
    def __init__(
        self,
        repository: UsersRepositoryProtocol,
        cache: UsersCacheProtocol = None,  # TO DO
    ):
        self.repository = repository
        self.cache = cache

    async def get_user_by_username_for_auth(self, username: str) -> UserEntity | None:
        return await self.repository.get_one_or_none_by_filters({'username': username})

    async def get_user_by_filters(self, filters: FiltersForSearchDTO):
        customer_entity: UserEntity = await self.repository.get_user_by_username_or_none(self.customer_username)
        search_user_username = filters.search_filters.get('username')
        search_user_id = filters.search_filters.get('id')
        # Если customer_entity не активен - raise InactiveUserError
        # Если customer_entity != username или не superuser/admin - raise UserPermissionsError
        customer_entity.check_permission_to_search_any_user(
            username_to_search=search_user_username,
            id_to_search=search_user_id,
        )
        if customer_entity.username == search_user_username or customer_entity.id == search_user_id:
            return customer_entity
        search_user_entity = await self.repository.get_one_or_none_by_filters(filters.search_filters)
        if search_user_entity is None:
            raise UserNotFoundByUsernameError
        return search_user_entity

    async def get_user_by_id_or_none(self, search_dto: SearchUserByIdDTO) -> UserEntity:
        if self.cache:
            user_entity: UserEntity = await self.cache.get_by_id(search_dto.search_user_id)
        else:
            user_entity: UserEntity = await self.repository.get_one_by_id_or_none(search_dto.search_user_id)
        if user_entity is None:
            raise UserNotFoundByIdError
        if not user_entity.is_active:
            raise InactiveUserError
        if user_entity.id != search_dto.search_user_id:
            user_entity.check_permission_to_search_any_user()
            user_entity: UserEntity = await self.repository.get_one_by_id_or_none(search_dto.search_user_id)
            if user_entity is None:
                raise UserNotFoundByIdError
        return user_entity

    async def get_all_users(self, users_dto: SearchUsersDTO) -> Sequence[UserEntity]:
        customer_user_entity: UserEntity = await self.repository.get_one_by_id_or_none(users_dto.customer_id)
        if customer_user_entity is None:
            raise UserNotFoundByIdError
        if not customer_user_entity.is_active:
            raise InactiveUserError
        customer_user_entity.check_permission_to_search_any_user()
        return await self.repository.get_many()

    async def create_user(self, create_user_dto: CreateUserDTO) -> UserEntity:
        logger.info('Запрос на создание нового пользователя: %r',create_user_dto)
        customer_user_entity: UserEntity = await self.repository.get_one_by_id_or_none(create_user_dto.customer_id)
        if customer_user_entity is None:
            logger.info(
                'Ошибка: инициатор с id=%r не найден.', create_user_dto.customer_id
            )
            raise UserNotFoundByIdError
        logger.info('Инициатор найден: %r', customer_user_entity.username)
        try:
            customer_user_entity.check_has_permission_to_crete_new_user()
        except UserPermissionsError:
            logger.info(
                'Ошибка: у инициатора %r нет прав на создание нового пользователя.',
                customer_user_entity.username,
            )
        if not check_set_password(create_user_dto.password):
            logger.info('Ошибка: Недопустимый пароль.')
            raise InvalidUserPasswordToSetError
        user_already_exists: UserEntity = await self.repository.get_one_or_none_by_filters(
            filters={'username': create_user_dto.username}
        )
        if user_already_exists:
            logger.info('Ошибка: пользователь %r уже существует.', user_already_exists.username)
            raise UserAlreadyExistsError
        entity = UserEntity(
            first_name=create_user_dto.first_name,
            last_name=create_user_dto.last_name,
            username=create_user_dto.username,
            password=hash_password(create_user_dto.password),
            email=create_user_dto.email,
            organization=Organizations(create_user_dto.organization),
            is_active=create_user_dto.is_active,
            is_admin=create_user_dto.is_admin,
            is_superuser=create_user_dto.is_superuser,
            role=Roles(create_user_dto.role),
            phone_number=create_user_dto.phone_number,
            telegram=create_user_dto.telegram,
            description=create_user_dto.description,
        )
        logger.info('Успешно создан новый пользователь: %r', entity)
        return await self.repository.add_user(entity)

    # async def create_user(self, data: CreateUserDTO) -> UserEntity:
    #     requestor_entity: UserEntity = (
    #         await self.repository.get_user_by_username_or_none(data.customer_id)
    #     )
    #     if requestor_entity is None:
    #         raise ForbiddenCreateError
    #     requestor_entity.has_permissions(Permissions.CREATE_USERS)
    #     if not check_set_password(data.password):
    #         raise InvalidPasswordToSetError
    #     if requestor_entity.username == data.username:
    #         raise UserAlreadyExistsError(data.username)
    #     user_already_exists = await self.repository.get_user_by_username_or_none(
    #         data.username
    #     )
    #     if user_already_exists:
    #         raise UserAlreadyExistsError(data.username)
    #     entity = UserEntity(
    #         id=None,
    #         first_name=data.first_name,
    #         last_name=data.last_name,
    #         username=data.username,
    #         password=hash_password(data.password),
    #         email=data.email,
    #         organization=Organizations(data.organization),
    #         is_active=data.is_active,
    #         is_admin=data.is_admin,
    #         is_superuser=data.is_superuser,
    #         role=Roles(data.role),
    #         phone_number=data.phone_number,
    #         telegram=data.telegram,
    #         description=data.description,
    #     )
    #     return await self.repository.add(entity)

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
            raise ForbiddenUpdateError('Изменение пароля запрещено.')
        to_update_entity_as_dict = asdict(to_update_entity)
        data_as_dict = asdict(data)
        for k, v in data_as_dict.items():
            if k not in to_update_entity_as_dict:
                raise UpdateError(f'Некорректное поле для изменения: {k!r}')
            if k is not None:
                to_update_entity_as_dict[k] = v
        UserEntity(**to_update_entity_as_dict) # Проверка, что данные для обновления валидны
        return await self.repository.update(**data_as_dict)