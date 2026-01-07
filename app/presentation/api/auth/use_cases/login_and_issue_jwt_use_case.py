import logging
from dataclasses import dataclass

from app_logging.dev.config import JWT_LOGGER
from application.use_cases.auth.user_login_use_case import UserLoginUseCaseImpl
from core.dto.auth import UserAuthDTO
from core.dto.tokens import TokenDataDTO
from presentation.api.auth.jwt_helper import JWTHelper
from core.users.entities.user import UserEntity


logger = logging.getLogger(JWT_LOGGER)


@dataclass(frozen=True, slots=True, kw_only=True)
class LoginAndIssueJWTUseCaseIml:

    user_login_use_case: UserLoginUseCaseImpl

    async def __call__(self, login_dto: UserAuthDTO) -> TokenDataDTO:
        user_entity:UserEntity = await self.user_login_use_case(login_dto)
        token_data = JWTHelper.issue_jwt(
            user_entity=user_entity,
            refresh_token=True,
        )
        logger.info("Для %r выпущены 'access' и 'refresh' jwt.", user_entity.username)
        return token_data