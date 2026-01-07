import logging
from dataclasses import dataclass

from app_logging.dev.config import AUTH_LOGGER
from application.interfaces.repositories.users_repo_interface import UsersRepositoryProtocol

from core.dto.auth import UserAuthDTO
from core.users.entities.user import UserEntity
from core.users.exceptions import InvalidUsernameOrPasswordError, InactiveUserError

logger = logging.getLogger(AUTH_LOGGER)


@dataclass(frozen=True, slots=True, kw_only=True)
class UserLoginUseCaseImpl:

    user_repository: UsersRepositoryProtocol

    async def __call__(self, auth_data: UserAuthDTO) -> UserEntity:
        logger.info('Аутентификация пользователя %r', auth_data.username)
        user_entity: UserEntity = await self.user_repository.get_one_or_none_by_filters({'username': auth_data.username})
        if user_entity is None:
            logger.info('Пользователь %r не найден.', auth_data.username)
            raise InvalidUsernameOrPasswordError
        if not user_entity.is_active:
            logger.info('Запрещено: пользователь %r не активен.', user_entity.username)
            raise InactiveUserError
        if not user_entity.validate_password(auth_data.password):
            logger.info('Неверный пароль.')
            raise InvalidUsernameOrPasswordError
        logger.info('Успешная аутентификация %r', user_entity.username)
        return user_entity

