from typing import Protocol

from application.interfaces.services.base_service_interface import BaseReadServiceProtocol, BaseServiceProtocol
from domain.regions.region_commands import (
    UpdateRegionCommand,
    CreateRegionCommand,
    DeleteRegionCommand,
)
from domain.regions.region_entity import RegionEntity


class RegionsReadServiceProtocol(
    BaseReadServiceProtocol[RegionEntity],
    Protocol,
):
    async def get_by_code_or_name(self, code_or_name: str | int) -> RegionEntity: ...
    async def try_by_code_or_name(self, code_or_name: str | int) -> RegionEntity | None: ...


class RegionsServiceProtocol(
    RegionsReadServiceProtocol,
    BaseServiceProtocol[RegionEntity, CreateRegionCommand, UpdateRegionCommand, DeleteRegionCommand],
    Protocol,
): ...
