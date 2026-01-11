from typing import Protocol, TypeVar, ClassVar, Any

from core.contracts.field_contracts_validators.common import id_field_contract
from core.contracts.contract_field_validator import FieldValidatorContract

TM = TypeVar('TM')
TE = TypeVar('TE')


def abstactmethod(args):
    pass


class BaseDBMapperProtocol(Protocol):
    entity: ClassVar

    id_contract: FieldValidatorContract = id_field_contract

    @classmethod
    @abstactmethod
    def fields_validate(cls, **fields: Any) -> bool: ...

    @classmethod
    def to_entity(cls, db_model: TM) -> TE: ...

    def to_model(self, entity: TE) -> TM: ...

    @classmethod
    def entity_validate(
        cls,
        **fields,
    ):
        """Проверка корректности полей путём создания модели."""
        return cls.entity(**fields)
