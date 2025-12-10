from collections.abc import Sequence

from application.interfaces.services.regions_crud import RegionsServiceProtocol
from core.dto.regions import CreateRegionsDTO, UpdateRegionsDTO
from core.regions.entities.region import RegionEntity


class RegionsCrudUseCaseImpl:
    def __init__(self, regions_service: RegionsServiceProtocol):
        self.regions_service = regions_service

    async def get_region_by_id(self, region_id: int) -> RegionEntity | None:
        return await self.regions_service.get_region_by_id_or_none(region_id)

    async def get_region_by_name(self, name: str) -> RegionEntity | None:
        return await self.regions_service.get_region_by_name_or_none(name)

    async def get_region_by_code(self, code: int) -> RegionEntity | None:
        return await self.regions_service.get_region_by_code_or_none(code)

    async def get_all_regions(self) -> Sequence[RegionEntity]:
        return await self.regions_service.get_all_regions()

    async def create_region(self, region: CreateRegionsDTO) -> RegionEntity:
       return await self.regions_service.create_region(region)

    async def update_region(self, region: UpdateRegionsDTO) -> RegionEntity:
        return await self.regions_service.update_region(region)

