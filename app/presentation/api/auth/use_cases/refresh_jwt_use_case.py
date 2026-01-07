import logging
from dataclasses import dataclass

from app_logging.dev.config import JWT_LOGGER
from application.interfaces.repositories.users_repo_interface import UsersRepositoryProtocol
from application.use_cases.users.get_user_use_case import GetUserUseCaseImpl
from core.dto.auth import UserAuthDTO
from core.users.entities.user import UserEntity
from core.users.exceptions import InvalidUsernameOrPasswordError, UserNotFoundError
from presentation.api.auth.jwt_helper import JWTHelper

logger = logging.getLogger(JWT_LOGGER)


@dataclass(frozen=True, slots=True, kw_only=True)
class RefreshJWTUseCaseImpl:

    users_use_case: GetUserUseCaseImpl

    async def __call__(
        self,
        *,
        username: str,
        refresh_token: bool = False,
    ):
        logger.info("Получен запрос 'refresh jwt' от пользователя %r.", username)
        try:
            user_entity: UserEntity = await self.users_use_case.get_active_user_or_raise(username)
        except UserNotFoundError:
            logger.warning('Пользователь %r не найден.', username)
            raise UserNotFoundError(f'Пользователь {username!r} не найден.')
        token_data = JWTHelper.issue_jwt( # TODO JWTHelper выделить в интерфейс
            user_entity=user_entity,
            refresh_token=refresh_token,
        )
        logger.info("Для %r выпущены 'access' jwt.", user_entity.username)
        return token_data

