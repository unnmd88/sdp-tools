import logging
from dataclasses import dataclass

from app_logging.dev.config import DOMAIN
from application.dto.users import UserDTO
from application.interfaces import UserServiceProtocol
from domain.enums.unsorted import TokenTypesEnum
from infrastructure.auth.jwt.jwt_service import JWTService

logger = logging.getLogger(DOMAIN)


@dataclass(frozen=True, slots=True, kw_only=True)
class GetActiveUserFromAccessJwtUseCase:
    user_service: UserServiceProtocol
    jwt_service: JWTService

    async def __call__(self,token: str) -> UserDTO:
        pass