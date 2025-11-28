from infrastructure.database.models.crud import BaseCrud, T
from infrastructure.database.models import Region
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status


class RegionsCrud(BaseCrud):
    model = Region

    @classmethod
    async def get_one_by_code_or_name_or_404(
        cls, session: AsyncSession, id_or_name: int | str
    ) -> T:
        if id_or_name.isdigit():
            stmt = select(cls.model).where(cls.model.code == int(id_or_name))
        else:
            stmt = select(cls.model).where(
                cls.model.name == id_or_name.replace(' ', '').capitalize()
            )
        res = await session.execute(stmt)
        if (region := res.scalars().one_or_none()) is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail='Region not found'
            )
        return region
