import logging
from dataclasses import dataclass

from app_logging.dev.config import AUTH_LOGGER
from application.dto.auth_dto import UserAuthDTO
from application.exceptions import AuthenticationError, InactiveAccountError
from application.interfaces import PasswordServiceProtocol, UserServiceProtocol
from domain.kernel.enums.validation_err_messages import ErrorMessages
from domain.users.user_entity import UserEntity

logger = logging.getLogger(AUTH_LOGGER)


@dataclass(frozen=True, slots=True, kw_only=True)
class AuthenticationService:
    """Сервис аутентификации."""

    user_service: UserServiceProtocol
    password_service: PasswordServiceProtocol

    async def authenticate(self, auth_dto: UserAuthDTO) -> UserEntity:
        """Аутентификация пользователя"""
        logger.info("Аутентификация пользователя %r", auth_dto.username)
        if (
            user := await self.user_service.try_get_user_by_username(
                username=auth_dto.username
            )
        ) is None:
            logger.info("Пользователь %r не найден в репозитории.", auth_dto.username)
            raise AuthenticationError(
                private_message=ErrorMessages.invalid_username_or_password
            )
        if not self.password_service.verify_password(
            password=auth_dto.password,
            hashed_password=user.password,
        ):
            logger.info("Неверный пароль для пользователя %r.", auth_dto.username)
            raise AuthenticationError(
                private_message=ErrorMessages.invalid_username_or_password
            )
        if not user.is_active:
            logger.info("Запрещено: пользователь %r не активен.", auth_dto.username)
            raise InactiveAccountError(private_message=ErrorMessages.inactive_user)
        logger.info("Аутентификация успешна для пользователя %r", auth_dto.username)
        return user
