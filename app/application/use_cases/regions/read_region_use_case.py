from dataclasses import dataclass

from application.dto.regions import RegionDTO
from application.interfaces.services.regions_service_interface import (
    RegionsServiceProtocol,
)

from domain.exceptions import DomainEntityNotFoundError


@dataclass(frozen=True, slots=True, kw_only=True)
class ReadRegionUseCaseImpl:
    regions_service: RegionsServiceProtocol

    async def by_id(self, region_id: int) -> RegionDTO:
        region = await self.regions_service.get_region_by_id(region_id)
        if region is None:
            raise DomainEntityNotFoundError(public_message="Регион не найден.")
        else:
            return RegionDTO.from_entity(region)

    async def by_code_or_name(self, region_code_or_name: int | str) -> RegionDTO:
        region = await self.regions_service.get_region_by_code_or_name(
            code_or_name=region_code_or_name,
            raise_if_not_found=True,
        )
        return RegionDTO.from_entity(region)

    async def get_many(
        self,
        skip: int = 0,
        limit: int = 100,
        order_by: list | None = None,
    ) -> list[RegionDTO]:
        return [
            RegionDTO.from_entity(region)
            for region in await self.regions_service.get_many(
                skip=skip, limit=limit, order_by=order_by
            )
        ]
