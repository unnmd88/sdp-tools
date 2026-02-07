from dataclasses import dataclass
from typing import final, ClassVar

from application.dto.users import UpdateUserDTO
from application.interfaces.mappers.db import BaseDBMapperProtocol


from domain.enums.unsorted import Roles, Organizations
from domain.entities.user_entity import UserEntity
from infrastructure.database.models import User as UserModel


@final
@dataclass(frozen=True, slots=True)
class UserDBMapper(BaseDBMapperProtocol):
    @classmethod
    def to_entity(cls, model: UserModel) -> UserEntity:
        """ """

        return UserEntity(
            id=model.id,
            firstname=model.first_name,
            lastname=model.last_name,
            username=model.username,
            organization=model.organization,
            email=model.email,
            password=model.password,
            is_active=model.is_active,
            role=model.role,
            phone_number=model.phone_number,
            telegram=model.telegram,
            description=model.description,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    @classmethod
    def to_model(cls, entity: UserEntity) -> UserModel:
        """ """
        return UserModel(
            first_name=entity.firstname,
            last_name=entity.lastname,
            username=entity.username,
            organization=entity.organization,
            email=entity.email,
            password=entity.password,
            is_active=entity.is_active,
            role=entity.role,
            phone_number=entity.phone_number,
            telegram=entity.telegram,
            description=entity.description,
        )
