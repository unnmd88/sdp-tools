from typing import TypeVar, Annotated

from sqlalchemy.ext.asyncio.session import AsyncSession

from infrastructure.database.models import Base
from infrastructure.database.api import db_api
from fastapi.params import Depends


T = TypeVar('T', bound=Base)


class BaseSqlAlchemy:
    model = T

    # def __init__(self, session: AsyncSession):
    def __init__(self, session: AsyncSession = None):
        self.session: AsyncSession = session

    async def get_one_by_id_or_none(self, _id: int):
        async with db_api.session_factory() as session:
            return await session.get(self.model, _id)

    async def get_all(self): ...

    async def add(self, entity): ...

    async def update(self, model): ...