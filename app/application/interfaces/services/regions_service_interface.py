from typing import Protocol

from domain.regions.region_commands import (
    UpdateRegionCommand,
    CreateRegionCommand,
    DeleteRegionCommand,
)
from domain.regions.region_entity import RegionEntity


class RegionsReadServiceProtocol(Protocol):
    async def get_by_id(self, region_id: int) -> RegionEntity: ...
    async def get_by_code_or_name(self, code_or_name: str | int) -> RegionEntity: ...
    async def get_many(
        self, skip: int, limit: int, order_by: list | None, **filters
    ) -> list[RegionEntity]: ...


class RegionsWriteServiceProtocol(Protocol):
    async def update(self, command: UpdateRegionCommand) -> RegionEntity: ...
    async def create(self, command: CreateRegionCommand) -> RegionEntity: ...
    async def delete(self, command: DeleteRegionCommand) -> RegionEntity: ...


class RegionsServiceProtocol(
    RegionsReadServiceProtocol, RegionsWriteServiceProtocol, Protocol
): ...
