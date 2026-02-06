from abc import abstractmethod
from typing import Protocol, Self


class UnitOfWorkProtocol(Protocol):

    @abstractmethod
    async def __aenter__(self) -> Self: ...
    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None: ...
    @abstractmethod
    async def commit(self) -> None: ...
    @abstractmethod
    async def rollback(self) -> None: ...

