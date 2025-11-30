from application.interfaces.repositories.base import BaseCrudProtocol
from application.interfaces.services.authentication import (
    AuthenticationUserServiceProtocol,
)
from auth.schemas import AuthSchema, TokenInfo
from infrastructure.database.user_reposirory import UsersRepositorySqlAlchemy


class AuthUseCaseImpl:
    def __init__(self, user_service: AuthenticationUserServiceProtocol):
        self.user_service = user_service

    async def auth_and_issue_jwt(
        self,
        refresh: bool,
    ) -> TokenInfo:
        return await self.user_service.auth_and_issue_jwt(refresh_token=refresh)
