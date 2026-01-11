from dataclasses import dataclass, asdict
from typing import final, Any, ClassVar

from application.interfaces.mappers.db import BaseDBMapperProtocol
from core.contracts.contract_field_validator import FieldValidatorContract
from core.contracts.field_contracts_validators.common import (
    created_at_field_contract,
    updated_at_field_contract,
)
from core.contracts.field_contracts_validators.user import (
    username_field_contract,
    firstname_field_contract,
    lastname_field_contract,
    organization_field_contract,
    email_field_contract,
    password_field_contract,
    is_active_field_contract,
    role_field_contract,
    phone_number_field_contract,
    telegram_field_contract,
    description_field_contract,
)
from core.dto.users import UpdateUserDTO
from core.enums import Roles, Organizations
from core.users.entities.user import UserEntity
from infrastructure.database.models import User as UserModel


@final
@dataclass(frozen=True, slots=True)
class UserDBMapper(BaseDBMapperProtocol):
    entity: ClassVar = UserEntity

    @classmethod
    def to_entity(cls, model: UserModel) -> UserEntity:
        """ """
        return UserEntity(
            id=cls.id_contract(model.id),
            firstname=firstname_field_contract(model.first_name),
            lastname=lastname_field_contract(model.last_name),
            username=username_field_contract(model.username),
            organization=organization_field_contract(model.organization),
            email=email_field_contract(model.email),
            password=password_field_contract(model.password),
            is_active=is_active_field_contract(model.is_active),
            role=role_field_contract(Roles(model.role)),
            phone_number=phone_number_field_contract(model.phone_number),
            telegram=telegram_field_contract(model.telegram),
            description=description_field_contract(model.description),
            created_at=created_at_field_contract(model.created_at),
            updated_at=updated_at_field_contract(model.updated_at),
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
            role=Roles(entity.role),
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
