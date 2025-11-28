from abc import abstractmethod
from typing import Protocol

from application.interfaces.repositories.base import BaseCrudProtocol
from application.interfaces.services.authentication import AuthenticationUserServiceProtocol
from auth.schemas import AuthSchema


class AuthUseCaseProtocol(Protocol):

    def __init__(self, user_service: AuthenticationUserServiceProtocol):
        self.user_service: AuthenticationUserServiceProtocol

    @abstractmethod
    async def auth_and_issue_jwt(
        self,
        refresh: bool,
    ):
        ...



