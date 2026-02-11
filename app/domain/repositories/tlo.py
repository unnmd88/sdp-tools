from domain.repositories.base_repo_interface import BaseCrudProtocol
from domain.traffic_light_objects.traffic_light_object_entity import TrafficLightObjectEntity


class TrafficLightObjectRepositoryProtocol(BaseCrudProtocol):
    async def get_tlo_by_name_or_none(
        self, name: str
    ) -> TrafficLightObjectEntity | None: ...

    async def get_base_tlo_by_name_or_none(
        self, name: str
    ) -> TrafficLightObjectEntity | None: ...
