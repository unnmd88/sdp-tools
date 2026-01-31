import logging
from dataclasses import dataclass

from app_logging.dev.config import AUTH_LOGGER
from application.dto.auth import UserAuthDTO
from application.dto.users import UserDTO
from application.exceptions import AuthenticationError, InactiveAccountError
from application.interfaces import PasswordServiceProtocol
from domain.enums.validation_err_messages import ErrorMessages
from domain.repositories.users_repo_interface import UsersRepositoryProtocol

logger = logging.getLogger(AUTH_LOGGER)


@dataclass(frozen=True, slots=True, kw_only=True)
class AuthenticationService:
    """Сервис аутентификации."""

    user_repository: UsersRepositoryProtocol
    password_service: PasswordServiceProtocol

    async def authenticate(self, auth_dto: UserAuthDTO) -> UserDTO | None:
        """Аутентификация пользователя"""
        logger.info("Аутентификация пользователя %r", auth_dto.username)
        if (
            user := await self.user_repository.get_by_username(auth_dto.username)
        ) is None:
            logger.info("Пользователь %r не найден в репозитории.", auth_dto.username)
            raise AuthenticationError(
                message=ErrorMessages.invalid_username_or_password
            )
        if not self.password_service.verify_password(
            password=auth_dto.password,
            hashed_password=user.password,
        ):
            logger.info("Неверный пароль для пользователя %r.", auth_dto.username)
            raise AuthenticationError(
                message=ErrorMessages.invalid_username_or_password
            )
        if not user.is_active:
            logger.info("Запрещено: пользователь %r не активен.", auth_dto.username)
            raise InactiveAccountError(message=ErrorMessages.inactive_user)
        logger.info("Аутентификация успешна для пользователя %r", auth_dto.username)
        return UserDTO.from_entity(user)
