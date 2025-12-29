from collections.abc import Sequence

from application.interfaces.services.regions_crud import RegionsServiceProtocol
from core.dto.filters import FiltersForSearchDTO
from core.dto.regions import CreateRegionDTO, UpdateRegionDTO, RegionFiltersForSearchDTO
from core.dto.update_entity import UpdatedEntityDTO
from core.regions.entities.region import RegionEntity


class RegionsCrudUseCaseImpl:
    def __init__(self, regions_service: RegionsServiceProtocol):
        self.regions_service = regions_service

    async def get_region_by_id(self, region_id: int) -> RegionEntity | None:
        return await self.regions_service.get_region_by_id_or_none(region_id)

    async def get_region_by_filters(self, filters: FiltersForSearchDTO) -> RegionEntity | None:
        return await self.regions_service.get_region_by_filters_or_none(filters)

    async def get_all_regions(self) -> Sequence[RegionEntity]:
        return await self.regions_service.get_all_regions()

    async def create_region(self, region: CreateRegionDTO) -> RegionEntity:
       return await self.regions_service.create_region(region)

    async def update_region(self, region: UpdateRegionDTO) -> UpdatedEntityDTO:
        return await self.regions_service.update_region(region)

    async def delete_region(self, _id: int) -> RegionEntity:
        return await self.regions_service.delete_region(_id)