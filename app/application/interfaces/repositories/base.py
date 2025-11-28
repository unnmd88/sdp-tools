from abc import abstractmethod
from typing import Protocol


class BaseCrudProtocol(Protocol):

    @abstractmethod
    async def get_one_by_id(self, _id: int): ...

    @abstractmethod
    async def get_all(self): ...

    @abstractmethod
    async def add(self, entity): ...

    @abstractmethod
    async def update(self, model): ...