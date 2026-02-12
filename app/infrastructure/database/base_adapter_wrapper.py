import logging
from dataclasses import dataclass
from typing import final

from sqlalchemy.ext.asyncio.session import AsyncSession

from app_logging.dev.config import INFRASTRUCTURE
from infrastructure.database.base_repository import BaseSqlAlchemyRepositoryAdapter
from infrastructure.database.utils import handle_db_errors


logger = logging.getLogger(INFRASTRUCTURE)


class BaseRepositoryAdapterWrapper[ModelType, T_Entity, BaseDBMapperProtocol]:
    def __init__(
        self,
        *,
        session: AsyncSession,
        model: type[ModelType],
        mapper: BaseDBMapperProtocol,
    ):
        self._base_repo_adapter = BaseSqlAlchemyRepositoryAdapter[
            ModelType, T_Entity, BaseDBMapperProtocol
        ](
            session=session,
            model=model,
            mapper=mapper,
        )
        self._session = session

    @handle_db_errors(logger=logger)
    async def try_by_id(self, _id: int) -> T_Entity | None:
        return await self._base_repo_adapter.get_by_id(_id)

    @handle_db_errors(logger=logger)
    async def try_by_filters(self, filters: dict) -> T_Entity | None:
        return await self._base_repo_adapter.get_one_or_none_by_filters(**filters)

    @handle_db_errors(logger=logger)
    async def get_many(
        self,
        skip: int = 0,
        limit: int | None = None,
        order_by: list | None = None,
        **filters,
    ) -> list[T_Entity]:
        return await self._base_repo_adapter.get_many(
            skip=skip,
            limit=limit,
            order_by=order_by,
            **filters,
        )

    async def create(self, entity: T_Entity) -> T_Entity:
        return await self._base_repo_adapter.add(entity)


