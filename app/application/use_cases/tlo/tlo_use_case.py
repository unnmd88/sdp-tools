from collections.abc import Sequence

from application.interfaces.services.tlo import TrafficLightObjectServiceProtocol
from core.tlo.entities.tlo import TrafficLightObjectEntity


class TrafficLightObjectUseCaseImpl:

    def __init__(self, tlo_service: TrafficLightObjectServiceProtocol):
        self.tlo_service = tlo_service

    async def get_tlo_by_id(self, tlo_id: int) -> TrafficLightObjectEntity | None:
        return await self.tlo_service.get_tlo_by_id_or_none(tlo_id)

    async def get_tlo_by_name(self, name: str) -> TrafficLightObjectEntity | None:
        return await self.tlo_service.get_tlo_by_name_or_none(name)

    async def get_all_tlo(self) -> Sequence[TrafficLightObjectEntity]:
        return await self.tlo_service.get_all_tlo()

    # async def create_tlo(self, region: CreateRegionsDTO) -> TrafficLightObjectEntity:
    #    return await self.regions_service.create_region(region)
    #
    # async def update_tlo(self, region: UpdateRegionsDTO) -> TrafficLightObjectEntity:
    #     return await self.regions_service.update_region(region)
