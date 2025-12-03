from typing import Protocol

from application.interfaces.repositories.users import UsersCrudRepositoryProtocol
from auth.schemas import AuthSchema, TokenInfo


class AuthenticationUserServiceProtocol(Protocol):
    def __init__(
        self,
        user_repository_factory: type[UsersCrudRepositoryProtocol],
        user_auth_schema: AuthSchema,
    ):
        self.repository: UsersCrudRepositoryProtocol
        self.user_auth_schema: AuthSchema

    async def auth_and_issue_jwt(
        self,
        refresh_token: bool,
    ) -> TokenInfo: ...
