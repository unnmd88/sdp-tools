from collections.abc import Sequence
from typing import Protocol

from application.interfaces.repositories.tlo import TrafficLightObjectRepositoryProtocol
from core.tlo.entities.tlo import TrafficLightObjectEntity
from core.users.entities.user import UserEntity



class TrafficLightObjectServiceProtocol(Protocol):

    def __init__(
        self,
        user_entity: UserEntity,
        repository: TrafficLightObjectRepositoryProtocol,
    ):
        self.user_entity = user_entity
        self.repository = repository

    async def get_base_tlo_by_id_or_none(self, _id: int) -> TrafficLightObjectEntity: ...

    async def get_tlo_by_name_or_none(self, name: str) -> TrafficLightObjectEntity: ...

    async def get_base_tlo_by_name_or_none(self, name: str) -> TrafficLightObjectEntity: ...

    async def get_all_tlo(self) -> Sequence[TrafficLightObjectEntity]: ...




    # async def create_region(self, tlo: CreateRegionsDTO) -> TrafficLightObjectEntity: ...
    #
    # async def update_region(self, tlo: UpdateRegionsDTO) -> TrafficLightObjectEntity: ...


