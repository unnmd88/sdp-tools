import logging

from sqlalchemy.ext.asyncio.session import AsyncSession

from app_logging.dev.config import INFRASTRUCTURE
from domain.entities.region_entity import RegionEntity
from infrastructure.database.base_repository import BaseSqlAlchemyRepository
from infrastructure.database.mappers.regions import RegionDBMapper
from infrastructure.database.models import Region as RegionModel
from infrastructure.database.utils import handle_db_errors

logger = logging.getLogger(INFRASTRUCTURE)


class RegionsSqlAlchemyRepository:
    def __init__(self, session: AsyncSession):
        self._repo = BaseSqlAlchemyRepository[RegionModel, RegionEntity, RegionDBMapper](
            session=session,
            model=RegionModel,
            mapper=RegionDBMapper(),
        )
        self._session = session

    @handle_db_errors(logger=logger)
    async def get_by_id(self, id: int) -> RegionEntity | None:
        return await self._repo.get_by_id(id)

    @handle_db_errors(logger=logger)
    async def get_by_filters(self, **filters) -> RegionEntity | None:
        return await self._repo.get_one_or_none_by_filters(**filters)

    async def get_by_code(self, region_code: int) -> RegionEntity | None:
        return await self._repo.get_one_or_none_by_filters(code=region_code)

    async def get_by_name(self, region_name: str) -> RegionEntity | None:
        return await self._repo.get_one_or_none_by_filters(name=region_name)

    @handle_db_errors(logger=logger)
    async def get_many(
        self,
        skip: int = 0,
        limit: int | None = None,
        order_by: list | None = None,
        **filters
    ) -> list[RegionEntity]:
        return await self._repo.get_many(
            skip=skip,
            limit=limit,
            order_by=order_by,
            **filters,
        )