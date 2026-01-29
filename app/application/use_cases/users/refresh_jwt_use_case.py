import logging
from dataclasses import dataclass

from jwt import ExpiredSignatureError

from app_logging.dev.config import AUTH_LOGGER
from application.dto.jwt_dto import TokenDataDTO

from domain.enums.validation_err_messages import ErrorMessages
from domain.repositories.users_repo_interface import UsersRepositoryProtocol
from infrastructure.auth.jwt.jwt_service import DecodeJWTService

from domain.enums.unsorted import TokenTypesEnum
from domain.entities.user import UserEntity

logger = logging.getLogger(AUTH_LOGGER)


@dataclass(frozen=True, slots=True, kw_only=True)
class RefreshJWTUseCaseImpl:
    user_repository: UsersRepositoryProtocol
    jwt_service: DecodeJWTService = DecodeJWTService

    async def __call__(self, refresh_jwt: bytes) -> TokenDataDTO:
        try:
            decoded_jwt = self.jwt_service.decode_jwt(refresh_jwt)
            if decoded_jwt.typ != TokenTypesEnum.refresh:
                logger.info(
                    "Неверный тип токена. Необходим refresh-токен. Payload: %r",
                    decoded_jwt,
                )
                raise UseCaseError(
                    message=ErrorMessages.invalid_token_type.format(
                        str(TokenTypesEnum.refresh)
                    )
                )
            user_entity: UserEntity = (
                await self.user_repository.get_one_or_none_by_filters(
                    {"username": decoded_jwt.sub}
                )
            )
            if user_entity is None:
                logger.info("Пользователь не найден. Payload: %r", decoded_jwt)
                raise UnauthorizedError(message="Пользователь не найден.")
            if not user_entity.is_active:
                raise ForbiddenError(message="Пользователь заблокирован.")

            return self.jwt_service.issue_access_jwt(UserDTO(**user_entity.to_dict()))
        except ExpiredSignatureError:
            raise UnauthorizedError(message="Срок действия токена истек.")
