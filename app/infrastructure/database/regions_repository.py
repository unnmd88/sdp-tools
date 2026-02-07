import logging
from collections.abc import Mapping

from sqlalchemy.ext.asyncio.session import AsyncSession

from app_logging.dev.config import INFRASTRUCTURE
from domain.entities.region_entity import RegionEntity
from infrastructure.database.base_repository import BaseSqlAlchemyRepositoryAdapter
from infrastructure.database.mappers.regions import RegionDBMapper
from infrastructure.database.models import Region as RegionModel
from infrastructure.database.utils import handle_db_errors
from infrastructure.exceptions import RepositoryCorruptedError

logger = logging.getLogger(INFRASTRUCTURE)


class RegionsSqlAlchemyRepository:
    def __init__(self, session: AsyncSession):
        self._base_repo_adapter = BaseSqlAlchemyRepositoryAdapter[
            RegionModel, RegionEntity, RegionDBMapper
        ](
            session=session,
            model=RegionModel,
            mapper=RegionDBMapper(),
        )
        self._session = session

    @handle_db_errors(logger=logger)
    async def get_by_id(self, id: int) -> RegionEntity | None:
        return await self._base_repo_adapter.get_by_id(id)

    @handle_db_errors(logger=logger)
    async def get_by_filters(self, filters: dict) -> RegionEntity | None:
        return await self._base_repo_adapter.get_one_or_none_by_filters(**filters)

    @handle_db_errors(logger=logger)
    async def get_by_code(self, region_code: int) -> RegionEntity | None:
        return await self._base_repo_adapter.get_one_or_none_by_filters(code=region_code)

    @handle_db_errors(logger=logger)
    async def get_by_name(self, region_name: str) -> RegionEntity | None:
        return await self._base_repo_adapter.get_one_or_none_by_filters(name=region_name)

    @handle_db_errors(logger=logger)
    async def get_many(
        self,
        skip: int = 0,
        limit: int | None = None,
        order_by: list | None = None,
        **filters,
    ) -> list[RegionEntity]:
        return await self._base_repo_adapter.get_many(
            skip=skip,
            limit=limit,
            order_by=order_by,
            **filters,
        )

    async def update(self, entity: RegionEntity) -> RegionEntity:
        model = await self._session.get(RegionModel, entity.id)
        if model is None:
            exc = RepositoryCorruptedError(
                private_message="Не найдена запись в базе данных по id из существующей сущности, полученной из БД"
            )
            logger.critical(exc.to_dict())
            raise exc
        updated_model = self._base_repo_adapter.mapper.update_model(model=model, entity=entity)
        await self._session.flush()
        await self._session.refresh(updated_model)
        return self._base_repo_adapter.mapper.to_entity(updated_model)

    async def add(self, entity: RegionEntity) -> RegionEntity:
        return await self._base_repo_adapter.add(entity)

    async def delete(self, _id: int) -> RegionEntity | None:
        return await self._base_repo_adapter.delete(_id)