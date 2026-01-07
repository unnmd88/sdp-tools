
import logging
from collections.abc import Sequence
from dataclasses import dataclass

from app_logging.dev.config import USERS_LOGGER
from application.interfaces.repositories.users_repo_interface import UsersRepositoryProtocol
from application.interfaces.use_cases.get_user_use_case_interface import GetUserUseCaseProtocol

from core.dto.users import CreateUserDTO
from core.enums import Permissions, Organizations, Roles
from core.exceptions.base import UserPermissionsError, ApplicationError

from core.users.entities.user import UserEntity
from core.users.exceptions import (
    UserNotFoundError,
    InactiveUserError,
    UserAlreadyExistsError,
    InvalidUserPasswordToSetError
)
from core.users.services.user_password import check_password_to_set_is_valid, hash_password

logger = logging.getLogger(USERS_LOGGER)


@dataclass(frozen=True, slots=True, kw_only=True)
class CreateUserUseCaseImpl:

    user_repository: UsersRepositoryProtocol
    get_user_use_case: GetUserUseCaseProtocol

    async def __call__(self, create_user_dto: CreateUserDTO) -> UserEntity:
        logger.info('Запрос на создание нового пользователя от инициатора=%r: %r' ,create_user_dto.username, create_user_dto)
        try:
            customer_entity: UserEntity = await self.get_user_use_case.get_active_user_or_raise(create_user_dto.customer)
            logger.info('Инициатор=%r найден', customer_entity.username)
        except UserNotFoundError:
            msg = f'Ошибка: {create_user_dto.customer!r} не найден.'
            logger.info(msg)
            raise UserNotFoundError(msg)
        except InactiveUserError:
            msg = f'Ошибка: {create_user_dto.customer!r} не активен.'
            logger.info(msg)
            raise InactiveUserError(msg)
        except ApplicationError as e:
            logger.critical('Ошибка логики создания нового пользователя: %r', e)
            raise
        if not customer_entity.permissions.has(Permissions.CREATE_USERS):
            msg = f'У {customer_entity.username!r} нет прав для создания пользователей.'
            logger.warning(msg)
            raise UserPermissionsError(msg)
        user_already_exists: UserEntity = await self.get_user_use_case.get_user_by_username_or_none(
            create_user_dto.username
        )
        if user_already_exists:
            msg = f'Пользователь с username={user_already_exists.username}(id={user_already_exists.id}) существует.'
            logger.warning(msg)
            raise UserAlreadyExistsError(msg)
        if create_user_dto.password == create_user_dto.username:
            msg = 'Ошибка: username и пароль должны отличаться'
            logger.info(msg)
            raise InvalidUserPasswordToSetError(msg)
        if not check_password_to_set_is_valid(create_user_dto.password):
            msg = 'Ошибка: username и пароль должны отличаться'
            logger.info(msg)
            raise InvalidUserPasswordToSetError('%s: %s', msg, create_user_dto.password)
        entity = UserEntity(
            first_name=create_user_dto.first_name,
            last_name=create_user_dto.last_name,
            username=create_user_dto.username,
            password=hash_password(create_user_dto.password),
            email=create_user_dto.email,
            organization=Organizations(create_user_dto.organization),
            is_active=create_user_dto.is_active,
            role=Roles(create_user_dto.role),
            phone_number=create_user_dto.phone_number,
            telegram=create_user_dto.telegram,
            description=create_user_dto.description,
        )
        logger.warning(entity)
        try:
            new_user_entity = await self.user_repository.add_user(entity)
            assert new_user_entity == entity
        except Exception as e:
            msg = f'Ошибка логики приложения при добавлении пользователя в репозиторий: {e}'
            logger.critical(msg)
            raise ApplicationError(msg)
        logger.info('Успешно создан новый пользователь: %r', new_user_entity)
        return new_user_entity
