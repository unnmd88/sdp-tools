from dataclasses import dataclass
from typing import final

from application.interfaces.mappers.db import BaseDBMapperProtocol
from domain.entities.passport_group_entity import PassportGroupEntity

from infrastructure.database.models import PassportGroup as PassportGroupModel


@final
@dataclass(frozen=True, slots=True)
class PassportGroupsDBMapper(
    BaseDBMapperProtocol[PassportGroupModel, PassportGroupEntity]
):
    @classmethod
    def to_entity(cls, model: PassportGroupModel) -> PassportGroupEntity:
        """ """
        return PassportGroupEntity(
            id=model.id,
            name=model.name,
            description=model.description,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @classmethod
    def to_model(cls, entity: PassportGroupEntity) -> PassportGroupModel:
        """ """
        return PassportGroupModel(
            name=entity.name,
            description=entity.description,
        )

    @classmethod
    def update_model(
        cls,
        *,
        model: PassportGroupModel,
        entity: PassportGroupEntity,
    ) -> PassportGroupModel:
        """ """
        model.description = entity.description
        model.name = entity.name
        return model
