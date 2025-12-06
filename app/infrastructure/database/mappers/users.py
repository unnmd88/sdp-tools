from dataclasses import dataclass
from typing import final

from application.interfaces.mappers.db import BaseDBMapperProtocol
from core.enums import Roles, Organizations
from core.users.entities.user import UserEntity
from infrastructure.database.models import User as UserModel


@final
@dataclass(frozen=True, slots=True)
class UserDBMapper(BaseDBMapperProtocol):
    @classmethod
    def to_entity(cls, model: UserModel) -> UserEntity:
        """ """
        return UserEntity(
            id=model.id,
            first_name=model.first_name,
            last_name=model.last_name,
            username=model.username,
            organization=Organizations(model.organization),
            email=model.email,
            password=model.password,
            is_active=model.is_active,
            is_admin=model.is_admin,
            is_superuser=model.is_superuser,
            role=Roles(model.role),
            phone_number=model.phone_number,
            telegram=model.telegram,
            description=model.description,
        )

    @classmethod
    def to_model(cls, entity: UserEntity) -> UserModel:
        """ """
        return UserModel(
            first_name=entity.first_name,
            last_name=entity.last_name,
            username=entity.username,
            organization=Organizations(entity.organization),
            email=entity.email,
            password=entity.password,
            is_active=entity.is_active,
            is_admin=entity.is_admin,
            is_superuser=entity.is_superuser,
            role=Roles(entity.role),
            phone_number=entity.phone_number,
            telegram=entity.telegram,
            description=entity.description,
        )
