from dataclasses import dataclass
from typing import final

from application.interfaces.mappers.db import BaseDBMapperProtocol
from core.enums import PassportGroups, PassportGroupsRoutes
from core.passport_groups.entities.passport_group import PassportGroupEntity
from infrastructure.database.models import PassportGroup as PassportGroupModel



@final
@dataclass(frozen=True, slots=True)
class PassportGroupsDBMapper(BaseDBMapperProtocol):
    @classmethod
    def to_entity(cls, model: PassportGroupModel) -> PassportGroupEntity:
        """ """
        return PassportGroupEntity(
            id=model.id,
            group_name=PassportGroups(model.group_name),
            group_name_route=PassportGroupsRoutes(model.group_name_route),
            description=model.description,
        )

    @classmethod
    def to_model(cls, entity: PassportGroupEntity) -> PassportGroupModel:
        """ """
        if entity.id is None:
            return PassportGroupModel(
                group_name=entity.group_name,
                group_name_route=entity.group_name_route,
                description=entity.description,
            )
        return PassportGroupModel(
            id=entity.id,
            group_name=entity.group_name,
            group_name_route=entity.group_name_route,
            description=entity.description,
            )