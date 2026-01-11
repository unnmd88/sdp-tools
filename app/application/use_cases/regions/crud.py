from collections.abc import Sequence

from core.dto.common import (
    CreateRecordDTO,
    FiltersForSearchDTO,
    ToUpdateRecordDTO,
    UpdatedRecordDTO,
)

# from core.dto.filters import FiltersForSearchDTO
from core.dto.regions import CreateRegionDTO, UpdateRegionDTO
from core.regions.entities.region import RegionEntity


# class RegionsCrudUseCaseImpl:
#     def __init__(self, regions_service: RegionsServiceProtocol):
#         self.regions_service = regions_service
#
#     async def get_region_by_id(self, region_id: int) -> RegionEntity | None:
#         return await self.regions_service.get_region_by_id_or_none(region_id)
#
#     async def get_region_by_filters(
#         self, filters: FiltersForSearchDTO
#     ) -> RegionEntity | None:
#         return await self.regions_service.get_region_by_filters_or_none(filters)
#
#     async def get_all_regions(self) -> Sequence[RegionEntity]:
#         return await self.regions_service.get_all_regions()
#
#     async def create_region(self, create_dto: CreateRecordDTO) -> RegionEntity:
#         return await self.regions_service.create_region(create_dto)
#
#     async def update_region(self, update_dto: ToUpdateRecordDTO) -> UpdatedRecordDTO:
#         return await self.regions_service.update_region(update_dto)
#
#     async def delete_region(
#         self, delete_dto: FiltersForSearchDTO
#     ) -> RegionEntity | None:
#         return await self.regions_service.delete_region(delete_dto)
