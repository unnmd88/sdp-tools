from application.interfaces.repositories.tlo import TrafficLightObjectRepositoryProtocol
from core.services import BaseService
from core.tlo.entities.tlo import TrafficLightObjectEntity


class TrafficLightObjectServiceImpl(BaseService):

    repository: TrafficLightObjectRepositoryProtocol

    async def get_tlo_by_name_or_none(self, name: str) -> TrafficLightObjectEntity:
        self.user_entity.check_permission_read_tlo()
        return await self.repository.get_tlo_by_name_or_none(name)