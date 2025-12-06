from dataclasses import dataclass
from typing import Protocol

from application.interfaces.services.users_crud import UsersServiceProtocol


@dataclass
class AuthenticationSchemaProtocol(Protocol):
    username: str
    password: str


class UserAuthenticationServiceProtocol(Protocol):
    def __init__(self, user_service: UsersServiceProtocol):
        self.user_service = user_service

    async def authenticate(
        self,
        auth_data: AuthenticationSchemaProtocol,
    ): ...
