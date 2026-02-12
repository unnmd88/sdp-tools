from typing import Protocol

from domain.traffic_light_objects.tlo_commands import CreateTrafficLightObjectCommand
from domain.traffic_light_objects.tlo_entity import TrafficLightObjectEntity


class BaseReadServiceProtocol[T_Entity](Protocol):
    async def get_by_id(self, _id: int) -> T_Entity: ...
    async def get_many(
        self,
        skip: int,
        limit: int,
        order_by: list | None,
        **filters
    ) -> list[T_Entity]: ...


class BaseWriteServiceProtocol[T_Entity, T_CommandCreate, T_CommandUpdate, T_CommandDelete](Protocol):
    # async def update(self, command) -> T_Entity: ...
    async def create(self, command: T_CommandCreate) -> T_Entity: ...
    # async def delete(self, command) -> T_Entity: ...


class BaseServiceProtocol(BaseReadServiceProtocol, BaseWriteServiceProtocol, Protocol): ...


