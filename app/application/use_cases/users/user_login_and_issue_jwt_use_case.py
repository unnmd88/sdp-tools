import logging
from dataclasses import dataclass

from app_logging.dev.config import AUTH_LOGGER
from application.dto.jwt_dto import TokenDataDTO, PayloadJWTDTO

from application.dto.auth_dto import UserAuthDTO

from application.interfaces import AuthServiceProtocol
from application.interfaces.services.issue_jwt_service_interface import (
    IssueJWTServiceProtocol,
)
from domain.users.user_entity import UserEntity

logger = logging.getLogger(AUTH_LOGGER)


@dataclass(frozen=True, slots=True, kw_only=True)
class UserLoginAndIssueJWTUseCaseImpl:
    auth_service: AuthServiceProtocol
    jwt_service: IssueJWTServiceProtocol

    async def __call__(self, auth_dto: UserAuthDTO) -> TokenDataDTO:
        user: UserEntity = await self.auth_service.authenticate(auth_dto)
        payload = PayloadJWTDTO(
            user_id=user.id,
            sub=user.username,
            role=user.role,
            organization=user.organization,
            email=user.email,
        )
        token_pair = self.jwt_service.issue_pair(payload_dto=payload)
        logger.debug(
            "Пользователю %r(id=%r) выпущены JWT: %r",
            user.username,
            user.id,
            token_pair,
        )
        return token_pair
