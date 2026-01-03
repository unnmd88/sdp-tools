from collections.abc import Sequence
from typing import Protocol

from application.interfaces.repositories.regions import RegionsRepositoryProtocol
from application.interfaces.services.users import UsersServiceProtocol
from core.dto.common import CreateRecordDTO, FiltersForSearchDTO, ToUpdateRecordDTO, UpdatedRecordDTO
# from core.dto.filters import FiltersForSearchDTO
from core.dto.regions import RegionDTO, UpdateRegionDTO, CreateRegionDTO
from core.regions.entities.region import RegionEntity
from core.users.entities.user import UserEntity


class RegionsServiceProtocol(Protocol):

    def __init__(
        self,
        user_entity: UserEntity,
        repository: RegionsRepositoryProtocol,
    ):
        self.user_entity = user_entity
        self.repository = repository

    async def get_region_by_filters_or_none(self, filters: FiltersForSearchDTO) -> RegionEntity | None: ...

    async def get_region_by_id_or_none(self, _id: int) -> RegionEntity: ...

    async def get_all_regions(self) -> Sequence[RegionEntity]: ...

    async def create_region(self, region: CreateRecordDTO) -> RegionEntity: ...

    async def update_region(self, region: ToUpdateRecordDTO) -> UpdatedRecordDTO: ...

    async def delete_region(self, filters: FiltersForSearchDTO) -> RegionEntity | None: ...