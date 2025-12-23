from collections.abc import Sequence
from typing import Protocol

from application.interfaces.repositories.regions import RegionsRepositoryProtocol
from application.interfaces.services.users_crud import UsersServiceProtocol
from core.dto.regions import RegionsDTO, UpdateRegionsDTO, CreateRegionsDTO
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

    async def get_region_by_name_or_none(self, name: str) -> RegionEntity: ...

    async def get_region_by_code_or_none(self, region_code: int) -> RegionEntity: ...

    async def get_region_by_id_or_none(self, _id: int) -> RegionEntity: ...

    async def get_all_regions(self) -> Sequence[RegionEntity]: ...

    async def create_region(self, region: CreateRegionsDTO) -> RegionEntity: ...

    async def update_region(self, region: UpdateRegionsDTO) -> RegionEntity: ...

