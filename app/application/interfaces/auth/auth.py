from typing import Protocol

from application.interfaces.services.authentication import AuthenticationUserServiceProtocol
from auth.schemas import AuthSchema, TokenInfo


class AuthUseCaseProtocol(Protocol):

    def __init__(
            self,
            user_service: AuthenticationUserServiceProtocol,
            user_schema: AuthSchema,
    ):
        self.user_service: AuthenticationUserServiceProtocol
        self.user_schema: AuthSchema

    async def auth_and_issue_jwt(
        self,
        # user_auth_schema: AuthSchema,
    ) -> TokenInfo:
        ...





