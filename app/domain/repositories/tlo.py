from domain.repositories.base_repo_interface import BaseCrudProtocol
from domain.tlo.entities.tlo import TrafficLightObjectEntity


class TrafficLightObjectRepositoryProtocol(BaseCrudProtocol):
    async def get_tlo_by_name_or_none(
        self, name: str
    ) -> TrafficLightObjectEntity | None: ...

    async def get_base_tlo_by_name_or_none(
        self, name: str
    ) -> TrafficLightObjectEntity | None: ...
