from dataclasses import dataclass
from typing import final

from application.interfaces.mappers.db import BaseDBMapperProtocol
from domain.entities.region_entity import RegionEntity
from infrastructure.database.models import Region as RegionModel


@final
@dataclass(frozen=True, slots=True)
class RegionDBMapper(BaseDBMapperProtocol):

    @classmethod
    def to_entity(cls, model: RegionModel) -> RegionEntity:
        """ """
        return RegionEntity(
            id=model.id,
            code=model.code,
            name=model.name,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @classmethod
    def to_model(cls, entity: RegionEntity) -> RegionModel:
        """ """
        return RegionModel(
            code=entity.code,
            name=entity.name,
        )
