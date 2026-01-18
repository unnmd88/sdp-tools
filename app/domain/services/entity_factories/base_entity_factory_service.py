from typing import Protocol, TypeVar, Self

from application.interfaces.mappers.db import abstactmethod
from domain.contracts.field_contracts.datetime_contract import ContractDateTimeField
from domain.contracts.field_contracts.integer_contract import ContractIntegerField


T_Entity = TypeVar("T_Entity")


class AbstractEntityFactoryService[T_Entity]:
    contract_id = ContractIntegerField(
        field_name="id",
        nullable=False,
        use_cache=True,
    )
    contract_created_at = ContractDateTimeField(
        field_name="created_at",
        use_cache=False,
        nullable=True,
    )
    contract_updated_at = ContractDateTimeField(
        field_name="updated_at",
        use_cache=False,
        nullable=True,
    )

    @classmethod
    @abstactmethod
    def create_existing(cls, **kwargs) -> T_Entity: ...

    @classmethod
    @abstactmethod
    def create_new(cls, **kwargs) -> T_Entity: ...
