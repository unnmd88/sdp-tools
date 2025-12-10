from sqlalchemy.sql.expression import select

from core.regions.entities.region import RegionEntity
from infrastructure.database.base_repository import BaseSqlAlchemy
from infrastructure.database.mappers.regions import RegionDBMapper
from infrastructure.database.models import Region


class RegionsRepositorySqlAlchemy(BaseSqlAlchemy):
    model = Region
    mapper = RegionDBMapper

    async def get_region_by_name_or_none(self, region_name: str) -> RegionEntity | None:
        return await self.get_one_or_none_by_filters(name=region_name)

    async def get_region_by_code_or_none(self, region_code: int) -> RegionEntity | None:
        return await self.get_one_or_none_by_filters(code=region_code)
