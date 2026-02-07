import logging

from sqlalchemy.ext.asyncio.session import AsyncSession

from app_logging.dev.config import INFRASTRUCTURE
from domain.entities.passport_group_entity import PassportGroupEntity
from infrastructure.database.base_repository import BaseSqlAlchemyRepositoryAdapter
from infrastructure.database.mappers.passport_groups import PassportGroupsDBMapper

from infrastructure.database.models import PassportGroup as PassportGroupModel
from infrastructure.database.utils import handle_db_errors


logger = logging.getLogger(INFRASTRUCTURE)


class PassportGroupsSqlAlchemyRepository:
    model = PassportGroupModel
    def __init__(self, session: AsyncSession):
        self._base_repo_adapter = BaseSqlAlchemyRepositoryAdapter[
            PassportGroupModel, PassportGroupEntity, PassportGroupsDBMapper
        ](
            session=session,
            model=PassportGroupModel,
            mapper=PassportGroupsDBMapper(),
        )
        self._session = session

    @handle_db_errors(logger=logger)
    async def get_by_id(self, id: int) -> PassportGroupEntity | None:
        return await self._base_repo_adapter.get_by_id(id)

    @handle_db_errors(logger=logger)
    async def get_by_filters(self, filters: dict) -> PassportGroupEntity | None:
        return await self._base_repo_adapter.get_one_or_none_by_filters(**filters)

    @handle_db_errors(logger=logger)
    async def get_many(
        self,
        skip: int = 0,
        limit: int | None = None,
        order_by: list | None = None,
        **filters,
    ) -> list[PassportGroupEntity]:
        return await self._base_repo_adapter.get_many(
            skip=skip,
            limit=limit,
            order_by=order_by,
            **filters,
        )

    async def add(self, entity: PassportGroupEntity) -> PassportGroupEntity:
        return await self._base_repo_adapter.add(entity)

    async def update(self, entity: PassportGroupEntity) -> PassportGroupEntity:
        return await self._base_repo_adapter.update(entity)

    async def delete(self, _id: int) -> PassportGroupEntity | None:
        return await self._base_repo_adapter.delete(_id)