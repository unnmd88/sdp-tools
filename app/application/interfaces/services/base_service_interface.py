from typing import Protocol


class BaseReadServiceProtocol[T_Entity](Protocol):
    async def get_by_id(self, _id: int) -> T_Entity: ...
    async def try_by_id(self, _id: int) -> T_Entity | None: ...
    async def get_many(
        self,
        skip: int,
        limit: int,
        order_by: list | None,
        **filters
    ) -> list[T_Entity]: ...


class BaseWriteServiceProtocol[T_Entity, T_CommandCreate, T_CommandUpdate, T_CommandDelete](Protocol):
    async def update(self, command: T_CommandUpdate) -> T_Entity: ...
    async def create(self, command: T_CommandCreate) -> T_Entity: ...
    async def delete(self, command: T_CommandDelete) -> T_Entity: ...


class BaseServiceProtocol[T_Entity, T_CommandCreate, T_CommandUpdate, T_CommandDelete](
    BaseReadServiceProtocol[T_Entity],
    BaseWriteServiceProtocol[T_Entity, T_CommandCreate, T_CommandUpdate, T_CommandDelete],
    Protocol
): ...


