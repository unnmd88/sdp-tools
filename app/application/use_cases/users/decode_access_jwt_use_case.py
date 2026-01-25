import logging
from dataclasses import dataclass

from app_logging.dev.config import AUTH_LOGGER
from application.interfaces.use_cases.get_user_use_case_interface import GetUserUseCaseProtocol
from domain.dto.users import UserDTO
from domain.exceptions.entity_not_found_exc import DomainEntityNotFoundError
from domain.exceptions.permissions_exc import DomainInactiveUserError
from domain.users.entities.user import UserEntity

from infrastructure.auth.jwt.decode_jwt_service import DecodeJWTService

from domain.dto.jwt_dto import AccessJWTPayloadDTO

logger = logging.getLogger(AUTH_LOGGER)


@dataclass(frozen=True, slots=True, kw_only=True)
class GetUserFromRepoByJWTUseCaseImpl:

    decode_service: DecodeJWTService = DecodeJWTService()
    get_user_use_case: GetUserUseCaseProtocol
    require_active_user: bool = True

    async def __call__(self, access_token: str) -> UserDTO:
        decoded_jwt = self.decode_service(access_token)
        user_entity: UserEntity = await self.get_user_use_case.get_user_by_username_or_raise(decoded_jwt.sub)
        if user_entity is None:
            raise DomainEntityNotFoundError(message=f"Пользователь {decoded_jwt.sub!r} не найден.")
        print(f"require_active_user: {self.require_active_user}")
        if self.require_active_user and not user_entity.is_active:
            raise DomainInactiveUserError(message=f"Пользователь {decoded_jwt.sub!r} не активен.")
        return UserDTO(**user_entity.to_dict())
