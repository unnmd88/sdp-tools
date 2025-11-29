from abc import abstractmethod
from typing import Protocol

from application.interfaces.services.get_user import UsersRepositoryServiceProtocol
from application.interfaces.use_cases.base_crud import BaseCrudUseCaseProtocol


class UsersRepositoryUseCaseProtocol(Protocol):

    def __init__(self, user_service: type[UsersRepositoryServiceProtocol]):
        self.user_service: UsersRepositoryServiceProtocol

    @abstractmethod
    async def get_user_by_username(self, username: str): ...

    @abstractmethod
    async def get_user_by_id(self, user_id: int): ...