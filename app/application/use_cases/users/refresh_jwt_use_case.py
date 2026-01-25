import logging
from dataclasses import dataclass

from jwt import ExpiredSignatureError, DecodeError


from app_logging.dev.config import AUTH_LOGGER
from application.interfaces.repositories.users_repo_interface import (
    UsersRepositoryProtocol,
)

from application.services.exceptions import UnauthorizedError, ForbiddenError, InvalidTokenTypeError
from application.services.jwt.jwt_service import BaseJWTService

from domain.dto.jwt_dto import TokenDataDTO
from domain.dto.users import UserDTO
from domain.enums.unsorted import TokenTypesEnum
from domain.users.entities.user import UserEntity

logger = logging.getLogger(AUTH_LOGGER)


@dataclass(frozen=True, slots=True, kw_only=True)
class RefreshJWTUseCaseImpl:
    user_repository: UsersRepositoryProtocol
    jwt_service: BaseJWTService = BaseJWTService

    async def __call__(self, refresh_jwt: bytes) -> TokenDataDTO:
        try:
            decoded_jwt = self.jwt_service.decode_jwt(refresh_jwt)
            if decoded_jwt.typ != TokenTypesEnum.refresh:
                logger.info("Неверный тип токена. Необходим refresh-токен. Payload: %r", decoded_jwt)
                raise InvalidTokenTypeError(message="Неверный тип токена. Необходим refresh-токен")
            user_entity: UserEntity = await self.user_repository.get_one_or_none_by_filters(
                {"username": decoded_jwt.sub}
            )
            if user_entity is None:
                logger.info("Пользователь не найден. Payload: %r", decoded_jwt)
                raise UnauthorizedError(message="Пользователь не найден.")
            if not user_entity.is_active:
                raise ForbiddenError(message="Пользователь заблокирован.")

            return self.jwt_service.issue_access_jwt(UserDTO(**user_entity.to_dict()))
        except ExpiredSignatureError:
            raise UnauthorizedError(message="Срок действия токена истек.")
