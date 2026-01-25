import logging
from dataclasses import dataclass

from app_logging.dev.config import AUTH_LOGGER
from application.services.exceptions import InvalidTokenTypeError, UnauthorizedError
from application.services.jwt.jwt_service import BaseJWTService
from domain.dto.jwt_dto import AccessJWTPayloadDTO
from domain.enums.unsorted import TokenTypesEnum
from jwt import ExpiredSignatureError, DecodeError, InvalidTokenError

logger = logging.getLogger(AUTH_LOGGER)


@dataclass(slots=True, frozen=True, kw_only=True)
class DecodeJWTService:
    """Декодирует JWT-токен и возвращает его payload"""

    jwt_service: BaseJWTService = BaseJWTService

    def __call__(self, access_token: str) -> AccessJWTPayloadDTO:
        try:
            decoded_jwt = self.jwt_service.decode_jwt(access_token)
            if decoded_jwt.typ != TokenTypesEnum.access:
                logger.info("Неверный тип токена. Необходим access-токен. Payload: %r", decoded_jwt)
                raise InvalidTokenTypeError(message="Неверный тип токена. Необходим refresh-токен")
            return decoded_jwt
        except ExpiredSignatureError:
            raise UnauthorizedError(message="Срок действия токена истек.")
        except (DecodeError, InvalidTokenError):
            logger.info("Неверный токен. Payload: %r", access_token)
            raise UnauthorizedError(message="Неверный токен.")

