from typing import TypeVar, Annotated

from sqlalchemy.ext.asyncio.session import AsyncSession

from infra.database import Base
from infra.database.api import db_api
from fastapi.params import Depends


T = TypeVar('T', bound=Base)


class BaseSqlAlchemy:
    model = T

    # def __init__(self, session: AsyncSession):
    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    async def get_one_by_id(self, _id: int):
        print(f'Session: {self.session}')


        async with db_api.session_factory() as session:
            return await session.get(self.model, _id)

    async def get_all(self): ...

    async def add(self, entity): ...

    async def update(self, model): ...