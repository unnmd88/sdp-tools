from application.interfaces.services.authentication import (
    UserAuthenticationServiceProtocol,
)
from application.jwt_utils import create_access_jwt, create_refresh_jwt
from core.dto.auth import UserAuthDTO
from core.users.entities.user import UserEntity

from presentation.schemas.jwt import TokenInfo


class AuthJWTUseCaseImpl:
    def __init__(self, auth_service: UserAuthenticationServiceProtocol):
        self.auth_service = auth_service

    async def auth_and_issue_jwt(
        self,
        user_auth_data: UserAuthDTO,
        refresh_token=None,
    ) -> TokenInfo:
        user_entity: UserEntity = await self.auth_service.authenticate(user_auth_data)
        return TokenInfo(
            access_token=create_access_jwt(user_entity),
            refresh_token=create_refresh_jwt(user_entity) if refresh_token else None,
        )

