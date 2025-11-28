from abc import abstractmethod
from typing import Protocol

from application.interfaces.repositories.base import BaseCrudProtocol


class BaseCrudUseCaseProtocol(Protocol):

    def __init__(self, repository: BaseCrudProtocol):
        self.repository = repository

    @abstractmethod
    async def get_one_by_id(self, entity_id: int): ...

    @abstractmethod
    async def get_all(self): ...


