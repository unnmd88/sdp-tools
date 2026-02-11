import logging
from dataclasses import dataclass

from app_logging.dev.config import AUTH_LOGGER
from application.dto.jwt_dto import TokenDataDTO, PayloadJWTDTO
from application.interfaces import UserServiceProtocol
from application.interfaces.services.issue_jwt_service_interface import (
    IssueJWTServiceProtocol,
)

from domain.exceptions import DomainEntityNotFoundError
from domain.kernel.enums.validation_err_messages import ErrorMessages

logger = logging.getLogger(AUTH_LOGGER)


@dataclass(frozen=True, slots=True, kw_only=True)
class RefreshJWTUseCaseImpl:
    user_service: UserServiceProtocol
    jwt_service: IssueJWTServiceProtocol

    async def __call__(self, user_id: int) -> TokenDataDTO:
        user = await self.user_service.try_get_user_by_id(user_id)
        if user is None:
            exc = DomainEntityNotFoundError(
                message=f"Пользователь c id={user_id} не найден. В токене указан неверный id пользователя.",
                public_message=ErrorMessages.service_unavailable,
                context={"use_case:": f"{self.__class__.__name__}"},
            )
            logger.critical(exc.to_dict())
            raise exc
        if not user.is_active:
            exc = DomainEntityNotFoundError(
                message=f"Пользователь c id={user_id} активен. Выпуск токена запрещен.",
                public_message=ErrorMessages.account_is_blocked,
                context={"use_case:": f"{self.__class__.__name__}"},
            )
            logger.warning(exc.to_dict())
            raise exc
        payload = PayloadJWTDTO(
            user_id=user.id,
            sub=user.username,
            role=user.role,
            organization=user.organization,
            email=user.email,
        )
        token_access = self.jwt_service.issue_access_jwt(payload_dto=payload)
        logger.info(
            "Пользователю %r(id=%r) выпущен access через refresh JWT: %r",
            user.username,
            user.id,
            token_access,
        )
        return token_access
