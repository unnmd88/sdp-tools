import logging
from dataclasses import dataclass

from app_logging.dev.config import AUTH_LOGGER
from application.interfaces.repositories.users_repo_interface import (
    UsersRepositoryProtocol,
)
from application.interfaces.services.user_password_service_interface import (
    UserPasswordServiceProtocol,
)
from application.services.exceptions import UnauthorizedError, ForbiddenError
from application.services.jwt.jwt_service import BaseJWTService

from domain.dto.auth import UserAuthDTO
from domain.dto.jwt_dto import TokenDataDTO
from domain.dto.users import UserDTO
from domain.users.entities.user import UserEntity
from application.services.password_service import UserPasswordService

logger = logging.getLogger(AUTH_LOGGER)


@dataclass(frozen=True, slots=True, kw_only=True)
class UserLoginAndIssueJWTUseCaseImpl:

    user_repository: UsersRepositoryProtocol
    user_password_service: type[UserPasswordServiceProtocol] = UserPasswordService
    jwt_service: BaseJWTService = BaseJWTService

    async def __call__(self, auth_data: UserAuthDTO) -> TokenDataDTO:
        logger.info("Аутентификация пользователя %r", auth_data.username)
        user_entity: UserEntity = await self.user_repository.get_one_or_none_by_filters(
            {"username": auth_data.username}
        )
        if user_entity is None:
            logger.info("Пользователь %r не найден.", auth_data.username)
            raise UnauthorizedError(message="Неверное имя пользователя или пароль.")
        if not user_entity.is_active:
            logger.info("Запрещено: пользователь %r не активен.", user_entity.username)
            raise ForbiddenError(message="Пользователь не активен.")

        if not self.user_password_service.verify_password(
            password=auth_data.password, hashed_password=user_entity.password
        ):
            logger.info("Неверный пароль.")
            raise UnauthorizedError(message="Неверное имя пользователя или пароль.")
        logger.info("Успешная аутентификация %r", user_entity.username)
        logger.info("User: %r", user_entity)
        return self.jwt_service.issue_pair(user_dto=UserDTO(**user_entity.to_dict()))
