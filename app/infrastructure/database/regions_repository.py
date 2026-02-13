import logging

from sqlalchemy.ext.asyncio.session import AsyncSession

from app_logging.dev.config import INFRASTRUCTURE
from domain.regions.region_entity import RegionEntity
from infrastructure.database.base_repository import BaseCrudSqlAlchemyRepositoryAdapter
from infrastructure.database.mappers.regions import RegionDBMapper
from infrastructure.database.models import Region as RegionModel
from infrastructure.database.utils import async_handle_db_errors

logger = logging.getLogger(INFRASTRUCTURE)


class RegionsSqlAlchemyRepository(BaseCrudSqlAlchemyRepositoryAdapter[RegionModel, RegionEntity]):

    def __init__(self, session: AsyncSession):
        super().__init__(session=session, model=RegionModel, mapper=RegionDBMapper())

    async def get_by_code(self, region_code: int) -> RegionEntity | None:
        return await self.get_filter_by(code=region_code)

    async def get_by_name(self, region_name: str) -> RegionEntity | None:
        return await self.get_filter_by(name=region_name)

