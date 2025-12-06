from application.dtos.auth import UserAuthDTO
from application.interfaces.services.authentication import (
    UserAuthenticationServiceProtocol,
)
from auth.create_tokens import create_access_jwt, create_refresh_jwt

from presentation.schemas.jwt import TokenInfo


# class AuthUseCaseImpl:
#
#     def __init__(self, user_service: UsersServiceProtocol):
#         self.user_service = user_service
#
#     async def auth_and_issue_jwt(
#         self,
#         auth_dto: UserAuthDTO,
#         refresh_token=None,
#     ) -> TokenInfo:
#         if (user_entity := await self.user_service.get_user_by_username_or_none(auth_dto.username)) is None:
#             raise InvalidUsernameOrPasswordException
#         password_is_valid = validate_password(
#             password=auth_dto.password_plain,
#             hashed_password=user_entity.password,
#         )
#         if not password_is_valid:
#             raise InvalidUsernameOrPasswordException
#         if not user_entity.is_active:
#             raise InactiveUserException(user_entity.username)
#         return TokenInfo(
#             access_token=create_access_jwt(user_entity),
#             refresh_token=create_refresh_jwt(user_entity) if refresh_token else None,
#         )
#
#         return await self.user_service.auth_and_issue_jwt(refresh_token=refresh)


class AuthJWTUseCaseImpl:
    def __init__(self, auth_service: UserAuthenticationServiceProtocol):
        self.auth_service = auth_service

    async def auth_and_issue_jwt(
        self,
        user_auth_data: UserAuthDTO,
        refresh_token=None,
    ) -> TokenInfo:
        user_entity = await self.auth_service.authenticate(user_auth_data)
        return TokenInfo(
            access_token=create_access_jwt(user_entity),
            refresh_token=create_refresh_jwt(user_entity) if refresh_token else None,
        )

        return await self.user_service.auth_and_issue_jwt(refresh_token=refresh)
