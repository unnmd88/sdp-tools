from dataclasses import dataclass, asdict
from typing import final, Any, ClassVar

from application.interfaces.mappers.db import BaseDBMapperProtocol


from domain.dto.users import UpdateUserDTO
from domain.enums.unsorted import Roles, Organizations
from domain.services.entity_factories.user_entity_factory_service import (
    UserEntityFactoryService,
)
from domain.users.entities.user import UserEntity
from infrastructure.database.models import User as UserModel


@final
@dataclass(frozen=True, slots=True)
class UserDBMapper(BaseDBMapperProtocol):
    entity: ClassVar = UserEntity

    @classmethod
    def to_entity(cls, model: UserModel) -> UserEntity:
        """ """
        return UserEntityFactoryService.create_existing(
            id=model.id,
            firstname=model.first_name,
            lastname=model.last_name,
            username=model.username,
            organization=Organizations(model.organization),
            email=model.email,
            password=model.password,
            is_active=model.is_active,
            role=Roles(model.role),
            phone_number=model.phone_number,
            telegram=model.telegram,
            description=model.description,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
        return UserEntity(
            id=model.id,
            firstname=model.firstname,
            lastname=model.lastname,
            username=model.username,
            organization=Organizations(model.organization),
            email=model.email,
            password=model.password,
            is_active=model.is_active,
            role=Roles(model.role),
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

    @classmethod
    def to_update_model(
        cls,
        entity: UserEntity,
        model: UserModel,
        data_to_update: UpdateUserDTO,
    ) -> UserModel:
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
