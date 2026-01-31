import logging
from dataclasses import dataclass

from app_logging.dev.config import AUTH_LOGGER
from application.dto.jwt_dto import TokenDataDTO, PayloadJWTDTO
from application.dto.users import UserDTO


from application.dto.auth import UserAuthDTO
from application.exceptions import AuthenticationError
from application.interfaces import AuthServiceProtocol
from application.interfaces.services.issue_jwt_service_interface import (
    IssueJWTServiceProtocol,
)


logger = logging.getLogger(AUTH_LOGGER)


@dataclass(frozen=True, slots=True, kw_only=True)
class UserLoginAndIssueJWTUseCaseImpl:
    auth_service: AuthServiceProtocol
    jwt_service: IssueJWTServiceProtocol

    async def __call__(self, auth_dto: UserAuthDTO) -> TokenDataDTO:
        user_dto: UserDTO = await self.auth_service.authenticate(auth_dto)
        payload = PayloadJWTDTO(
            user_id=user_dto.id,
            sub=user_dto.username,
            role=user_dto.role,
            organization=user_dto.organization,
            email=user_dto.email,
        )
        try:
            token_pair = self.jwt_service.issue_pair(payload_dto=payload)
            logger.info(
                "Пользователю %r(id=%r) выпущены JWT: %r",
                user_dto.username,
                user_dto.id,
                token_pair,
            )
            return self.jwt_service.issue_pair(payload_dto=payload)
        except Exception as e:
            logger.error("Программная ошибка выпуска JWT: %r", str(e))
            raise AuthenticationError


# @dataclass(frozen=True, slots=True, kw_only=True)
# class UserLoginAndIssueJWTUseCaseImpl:
#     user_repository: UsersRepositoryProtocol
#     user_password_service: PasswordServiceProtocol = BcryptPasswordService()
#     jwt_service: JWTServiceProtocol
#
#     async def __call__(self, auth_data: UserAuthDTO) -> TokenDataDTO:
#         logger.info("Аутентификация пользователя %r", auth_data.username)
#         user_entity: UserEntity = await self.user_repository.get_one_or_none_by_filters(
#             {"username": auth_data.username}
#         )
#         if user_entity is None:
#             logger.info("Пользователь %r не найден.", auth_data.username)
#             raise AuthenticationError(message=ErrorMessages.invalid_username_or_password)
#         if not user_entity.is_active:
#             logger.info("Запрещено: пользователь %r не активен.", user_entity.username)
#             raise InactiveAccountError(message="Пользователь %r не активен.".format(user_entity.username))
#
#         if not self.user_password_service.verify_password(
#             password=auth_data.password, hashed_password=user_entity.password
#         ):
#             logger.info("Неверный пароль.")
#             raise UnauthorizedError(message=ErrorMessages.invalid_username_or_password)
#         logger.info("Успешная аутентификация %r", user_entity.username)
#         logger.info("User: %r", user_entity)
#         token_data = self.jwt_service.issue_pair(user_dto=UserDTO(**user_entity.to_dict()))
#         logger.info("Выпущены JWT: %r", token_data)
#         return self.jwt_service.issue_pair(user_dto=UserDTO(**user_entity.to_dict()))
