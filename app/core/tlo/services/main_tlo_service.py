from collections.abc import Sequence

from application.interfaces.repositories.tlo import TrafficLightObjectRepositoryProtocol
from core.services import BaseService
from core.tlo.entities.tlo import TrafficLightObjectEntity


class TrafficLightObjectServiceImpl(BaseService):

    repository: TrafficLightObjectRepositoryProtocol

    async def get_tlo_by_name_or_none(self, name: str) -> TrafficLightObjectEntity:
        self.user_entity.access_control_read_tlo()
        return await self.repository.get_tlo_by_name_or_none(name)

    async def get_base_tlo_by_name_or_none(self, name: str) -> TrafficLightObjectEntity:
        self.user_entity.access_control_read_tlo()
        return await self.repository.get_base_tlo_by_name_or_none(name)

    async def get_all_tlo(self) -> Sequence[TrafficLightObjectEntity]:
        self.user_entity.access_control_read_tlo()
        return await self.repository.get_all()