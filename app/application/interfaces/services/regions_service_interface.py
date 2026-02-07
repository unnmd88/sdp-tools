from typing import Protocol, Any

from domain.cqrs.region_commands import (
    UpdateRegionCommand,
    CreateRegionCommand,
    DeleteRegionCommand,
)
from domain.entities.region_entity import RegionEntity


class RegionsReadServiceProtocol(Protocol):
    async def get_region_by_and_filters(self, **filters) -> RegionEntity | None: ...
    async def get_region_by_id(self, id: int) -> RegionEntity | None: ...
    async def get_region_by_code_or_name(
        self,
        *,
        code_or_name: str | int,
        raise_if_not_found: bool,
    ) -> RegionEntity | None: ...
    async def get_region_by_id_or_raise(self, _id: int) -> RegionEntity: ...
    async def get_many(
        self,
        skip: int,
        limit: int,
        order_by: list | None,
    ) -> list[RegionEntity]: ...


class RegionsWriteServiceProtocol(Protocol):
    async def update_region(self, command: UpdateRegionCommand) -> RegionEntity: ...
    async def add_new_region(self, command: CreateRegionCommand) -> RegionEntity: ...
    async def delete_region(self, command: DeleteRegionCommand) -> None: ...


class RegionsServiceProtocol(
    RegionsReadServiceProtocol, RegionsWriteServiceProtocol, Protocol
): ...
