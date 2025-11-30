from collections.abc import Sequence
from typing import TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio.session import AsyncSession

from infrastructure.database.models import Base
from infrastructure.database.api import db_api
from fastapi.params import Depends


T = TypeVar('T', bound=Base)
Record = TypeVar('Record', bound=Base)


class BaseSqlAlchemy:
    model = T

    # def __init__(self, session: AsyncSession):
    def __init__(self, session: AsyncSession = None):
        self.session: AsyncSession = session

    async def get_one_by_id_or_none(self, _id: int) -> T | None:
        return await self.session.get(self.model, _id)

        async with db_api.session_factory() as session:
            return await session.get(self.model, _id)

    async def get_all(self, **filters) -> Sequence[T]:
        # if filters:
        #     filter_dict = filters.model_dump(exclude_unset=True)
        # else:
        #     filter_dict = {}
        stmt = select(self.model).filter_by(**filters)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def add(self, entity): ...

    async def update(self, model): ...
