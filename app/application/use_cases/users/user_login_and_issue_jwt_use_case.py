import logging
from dataclasses import dataclass, field
from functools import cached_property

from app_logging.dev.config import AUTH_LOGGER
from application.dtos.jwt_dto import TokenDataDTO, PayloadJWTDTO

from application.dtos.auth_dto import UserAuthDTO
from application.exceptions import AuthenticationError, InactiveAccountError, ApplicationLayerError

from application.interfaces import AuthServiceProtocol
from application.interfaces.services.issue_jwt_service_interface import (
    IssueJWTServiceProtocol,
)
from application.interfaces.services.user_service_interface import UserReadServiceProtocol
from domain.exceptions import DomainEntityNotFoundError
from domain.users.user_entity import UserEntity

logger = logging.getLogger(AUTH_LOGGER)


@dataclass(frozen=True, slots=True, kw_only=True)
class UserLoginAndIssueJWTUseCaseImpl:

    user_reader: UserReadServiceProtocol
    auth_service: AuthServiceProtocol
    jwt_service: IssueJWTServiceProtocol
    _fake_hash: str = field(init=False, default=b"$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj2cFZx8Jp3S")

    async def __call__(self, auth_dto: UserAuthDTO) -> TokenDataDTO:

        logger.info("Аутентификация пользователя %r", auth_dto.username)
        try:
            user = await self.user_reader.get_by_username(username=auth_dto.username)
        except DomainEntityNotFoundError:
            # fake auth
            self.auth_service.authenticate(
                plain_password=auth_dto.password,
                hashed_password=self._fake_hash,
            )
            logger.info("Пользователь %r не найден в репозитории.", auth_dto.username)
            raise AuthenticationError
        is_authenticated = self.auth_service.authenticate(
            plain_password=auth_dto.password,
            hashed_password=user.password,
        )
        if not is_authenticated:
            logger.info("Неверный пароль для пользователя %r.", auth_dto.username)
            raise AuthenticationError
        if not user.is_active:
            logger.info("Запрещено: пользователь %r не активен.", auth_dto.username)
            raise InactiveAccountError
        if not is_authenticated and not user.is_active:
            raise ApplicationLayerError(
                private_message="Неверный пароль и пользователь не активен. Некорректная проверка аутентификации.",
                is_authenticated=is_authenticated,
                user_is_active=user.is_active,
            )
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

