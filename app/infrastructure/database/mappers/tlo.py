from dataclasses import dataclass
from typing import final

from application.interfaces.mappers.db import BaseDBMapperProtocol
from core.dto.tlo import TrafficLightObjectDTO
from infrastructure.database.models import TrafficLightObject as TrafficLightObjectModel


@final
@dataclass(frozen=True, slots=True)
class TrafficLightObjectDBMapper(BaseDBMapperProtocol):
    @classmethod
    def to_tlo_dto(cls, model: TrafficLightObjectModel) -> TrafficLightObjectDTO:
        """ """

        id: int
        region_id: int
        name: str
        district: str
        street: str
        service_organization: ServiceOrganizations
        description: str
        created_at: datetime
        updated_at: datetime

        return TrafficLightObjectDTO(
            id=
            region_id=
            name=
            district=
            street=
            service_organization: ServiceOrganizations
            description=
            created_at: datetime
            updated_at: datetime

            id=model.id,
            code=RegionCodes(model.code),
            name=RegionNames(model.name),
        )

    @classmethod
    def to_model(cls, entity: RegionEntity) -> RegionModel:
        """ """
        if entity.id is None:
            return RegionModel(
                code=entity.code,
                name=entity.name,
            )
        return RegionModel(
            id=entity.id,
            code=entity.code,
            name=entity.name,
            )
