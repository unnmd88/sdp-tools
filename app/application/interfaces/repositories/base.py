from abc import abstractmethod
from typing import Protocol

from core.users.schemas import UserFromDbFullSchema


class BaseCrudProtocol(Protocol):
    async def get_one_by_id_or_none(self, _id: int): ...

    async def get_all(self): ...

    async def add(self, entity): ...

    async def update(self, model): ...
