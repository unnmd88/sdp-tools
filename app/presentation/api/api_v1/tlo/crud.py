from collections.abc import Sequence

from infrastructure.database.models.crud import BaseCrud, T
from infrastructure.database.models import TrafficLightObject
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload


class TloCrud(BaseCrud):
    model = TrafficLightObject

    @classmethod
    async def get_all(
        cls,
        session: AsyncSession,
        filters: BaseModel = None,
    ) -> Sequence[T]:
        filter_dict = filters.model_dump(exclude_unset=True) if filters else {}
        # query = select(cls.model).filter_by(**filter_dict)
        stmt = (
            select(
                cls.model,
                # TrafficLightObject.id,
                # TrafficLightObject.name,
                # Region.code,
                # Region.name,
                # TrafficLightObject.district,
                # TrafficLightObject.street,
                # TrafficLightObject.service_organization,
                # TrafficLightObject.description,
            )
            .options(joinedload(TrafficLightObject.region))
            .order_by(TrafficLightObject.id)
            .filter_by(**filter_dict)
        )

        # stmt = (
        #     select(cls.model)
        #     .join(TrafficLightObject.region_id)
        #     # .options(
        #     #     contains_eager(TrafficLightObject.region_id)
        #     #     .contains_eager(Region.name)
        #     # )
        #     .order_by(TrafficLightObject.id)
        #     .filter_by(**filter_dict)
        # )

        result = await session.execute(stmt)
        s = result.scalars().all()
        print(f'>>>>> s: {s}')
        print(f'>>>>> s[0]: {s[0].region}')
        return s
