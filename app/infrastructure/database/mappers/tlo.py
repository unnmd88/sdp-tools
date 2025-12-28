from dataclasses import dataclass
from datetime import datetime
from typing import final

from application.interfaces.mappers.db import BaseDBMapperProtocol
from core.dto.tlo import TrafficLightObjectDTO
from core.enums import ServiceOrganizations, RegionNames
from core.tlo.entities.tlo import TrafficLightObjectEntity
from infrastructure.database.models import TrafficLightObject as TrafficLightObjectModel


@final
@dataclass(frozen=True, slots=True)
class TrafficLightObjectDBMapper(BaseDBMapperProtocol):
    @classmethod
    def to_entity(cls, model: TrafficLightObjectModel) -> TrafficLightObjectEntity:
        """ """

        return TrafficLightObjectEntity(
            id=model.id,
            name=model.name,
            region=RegionNames.MOSCOW,
            latitude=.0,
            longitude=.0,
            district=model.district,
            street=model.street,
            service_organization=ServiceOrganizations(model.service_organization),
            traffic_controller=None,
            current_passport=None,
            description=model.description,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    # @classmethod
    # def to_model(cls, entity: RegionEntity) -> RegionModel:
    #     """ """
    #     if entity.id is None:
    #         return RegionModel(
    #             code=entity.code,
    #             name=entity.name,
    #         )
    #     return RegionModel(
    #         id=entity.id,
    #         code=entity.code,
    #         name=entity.name,
    #         )
