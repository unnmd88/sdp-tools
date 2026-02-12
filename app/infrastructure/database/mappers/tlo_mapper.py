from dataclasses import dataclass
from typing import final

from application.interfaces.mappers.db import BaseDBMapperProtocol
from domain.traffic_light_objects.tlo_entity import TrafficLightObjectEntity
from infrastructure.database.models import TrafficLightObject as TLOModel


@final
@dataclass(frozen=True, slots=True)
class TrafficLightObjectDBMapper(BaseDBMapperProtocol[TLOModel, TrafficLightObjectEntity]):
    @classmethod
    def to_entity(cls, model: TLOModel) -> TrafficLightObjectEntity:
        """ """
        return TrafficLightObjectEntity(
            id=model.id,
            region_id=model.region_id,
            created_by_user_id=model.created_by_user_id,
            updated_by_user_id=model.updated_by_user_id,
            name=model.name,
            traffic_controller_type=model.traffic_controller_type,
            latitude=model.latitude,
            longitude=model.longitude,
            district=model.district,
            address=model.address,
            note=model.note,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @classmethod
    def to_model(cls, entity: TrafficLightObjectEntity) -> TLOModel:
        """ """
        return TLOModel(
            region_id=entity.region_id,
            created_by_user_id=entity.created_by_user_id,
            updated_by_user_id=entity.updated_by_user_id,
            name=entity.name,
            traffic_controller_type=entity.traffic_controller_type,
            latitude=entity.latitude,
            longitude=entity.longitude,
            district=entity.district,
            address=entity.address,
            note=entity.note,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    @classmethod
    def update_model(
        cls,
        *,
        model: TLOModel,
        entity: TrafficLightObjectEntity,
    ) -> TLOModel:
        """ """
        model.region_id = entity.region_id
        model.name = entity.name
        model.note = entity.note
        model.updated_by_user_id = entity.updated_by_user_id
        model.latitude = entity.latitude
        model.longitude = entity.longitude
        model.district = entity.district
        model.address = entity.address
        model.traffic_controller_type = entity.traffic_controller_type
        return model

