from datetime import datetime

from domain.contract2.contract_field import ContractField
from domain.contract2.require import Require
from domain.entities.base_entity import Entity
from domain.entities_public_attrs import REGIONS_PUBLIC_ATTRS
from domain.enums.attrs_names import PublicAttrNamesEnum
from domain.enums.unsorted import RegionCodes, RegionNames
from domain.validators.positive_int_validator import IntegerValidator
from domain.validators.string_validator import StringValidator

T_ALLOWED_REGIONS = frozenset[tuple[RegionNames, RegionCodes]]


class RegionEntity(Entity):
    __public_attrs__ = REGIONS_PUBLIC_ATTRS

    code = ContractField(
        field_name=str(PublicAttrNamesEnum.code),
        nullable=False,
        use_cache=True,
        requires=[Require(handler=IntegerValidator(min_value=1, max_value=100_000))],
    )
    name = ContractField(
        field_name=str(PublicAttrNamesEnum.name),
        nullable=False,
        use_cache=True,
        requires=[Require(handler=StringValidator(min_length=1, max_length=32))],
    )

    @classmethod
    def create_new_region(
        cls,
        *,
        code: int,
        name: str,
    ):
        return cls(
            id=None,
            code=code,
            name=name,
        )

    def __init__(
        self,
        *,
        id: int | None,
        code: int,
        name: str,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
    ):
        super().__init__(id=id, created_at=created_at, updated_at=updated_at)
        self.code = code
        self.name = name


if __name__ == "__main__":
    r = RegionEntity.create_new_region(code=1, name="Москва")
