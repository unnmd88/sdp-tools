from dataclasses import dataclass

from application.dto.regions import RegionDTO
from application.interfaces.services.regions_service_interface import (
    RegionsReadServiceProtocol,
)


@dataclass(slots=True, kw_only=True, frozen=True)
class RegionReadByCodeOrNameUseCase:
    regions_service: RegionsReadServiceProtocol

    async def __call__(self, passport_group_name: str) -> RegionDTO:
        entity = await self.regions_service.get_by_code_or_name(passport_group_name)
        return RegionDTO.from_entity(entity)
