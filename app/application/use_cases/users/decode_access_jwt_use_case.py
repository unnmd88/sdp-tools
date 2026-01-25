import logging
from dataclasses import dataclass

from jwt import ExpiredSignatureError, DecodeError


from app_logging.dev.config import AUTH_LOGGER
from application.interfaces.repositories.users_repo_interface import (
    UsersRepositoryProtocol,
)

from application.services.exceptions import UnauthorizedError, ForbiddenError, InvalidTokenTypeError
from application.services.jwt.decode_jwt_service import DecodeJWTService
from application.services.jwt.jwt_service import BaseJWTService

from domain.dto.jwt_dto import TokenDataDTO, AccessJWTPayloadDTO
from domain.dto.users import UserDTO
from domain.enums.unsorted import TokenTypesEnum
from domain.users.entities.user import UserEntity

logger = logging.getLogger(AUTH_LOGGER)


@dataclass(frozen=True, slots=True, kw_only=True)
class DecodeJWTUseCaseImpl:

    decode_service: DecodeJWTService = DecodeJWTService()

    def __call__(self, access_token: str) -> AccessJWTPayloadDTO:
        return self.decode_service(access_token)
