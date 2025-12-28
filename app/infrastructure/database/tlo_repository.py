from core.tlo.entities.tlo import TrafficLightObjectEntity
from infrastructure.database.mappers.tlo import TrafficLightObjectDBMapper
from infrastructure.database.models import TrafficLightObject as TrafficLightModel
from infrastructure.database.base_repository import BaseSqlAlchemy


class TrafficLightObjectSqlAlchemy(BaseSqlAlchemy):

    model = TrafficLightModel
    mapper = TrafficLightObjectDBMapper

    async def get_tlo_by_name_or_none(self, tlo_name: str) -> TrafficLightObjectEntity | None:
        return await self.get_one_or_none_by_filters(name=tlo_name)