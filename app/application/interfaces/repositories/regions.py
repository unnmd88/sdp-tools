from application.interfaces.repositories.base import BaseCrudProtocol
from core.regions.entities.region import RegionEntity


class RegionsRepositoryProtocol(BaseCrudProtocol):

    async def get_region_by_name_or_none(self, name: str) -> RegionEntity | None: ...

    async def get_region_by_code_or_none(self, region_code: int) -> RegionEntity | None: ...