import logging
from dataclasses import dataclass

from app_logging.dev.config import AUTH_LOGGER
from application.interfaces.repositories.users_repo_interface import (
    UsersRepositoryProtocol,
)
from application.interfaces.services.user_password_service_interface import (
    UserPasswordServiceProtocol,
)

from domain.dto.auth import UserAuthDTO
from domain.users.entities.user import UserEntity
from domain.services.user_password_service import UserPasswordService

logger = logging.getLogger(AUTH_LOGGER)


@dataclass(frozen=True, slots=True, kw_only=True)
class UserLoginUseCaseImpl:
    user_repository: UsersRepositoryProtocol
    user_password_service: type[UserPasswordServiceProtocol] = UserPasswordService

    async def __call__(self, auth_data: UserAuthDTO) -> UserEntity:
        logger.info("Аутентификация пользователя %r", auth_data.username)
        user_entity: UserEntity = await self.user_repository.get_one_or_none_by_filters(
            {"username": auth_data.username}
        )
        if user_entity is None:
            logger.info("Пользователь %r не найден.", auth_data.username)
            raise InvalidUsernameOrPasswordError
        if not user_entity.is_active:
            logger.info("Запрещено: пользователь %r не активен.", user_entity.username)
            raise InactiveUserError

        if not self.user_password_service.verify_password(
            password=auth_data.password, hashed_password=user_entity.password
        ):
            logger.info("Неверный пароль.")
            raise InvalidUsernameOrPasswordError
        logger.info("Успешная аутентификация %r", user_entity.username)
        logger.info("User: %r", user_entity)
        return user_entity
