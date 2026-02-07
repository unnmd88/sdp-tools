from datetime import datetime

from domain.contract2.contract_field import ContractField
from domain.contract2.require import Require
from domain.entities.base_entity import Entity
from domain.entities_public_attrs import PASSPORT_GROUPS_PUBLIC_ATTRS
from domain.enums.attrs_names import PublicAttrNamesEnum
from domain.validators.string_validator import StringValidator


class PassportGroupEntity(Entity):
    __public_attrs__ = PASSPORT_GROUPS_PUBLIC_ATTRS

    name = ContractField(
        field_name=str(PublicAttrNamesEnum.name),
        nullable=False,
        use_cache=True,
        requires=[Require(handler=StringValidator(min_length=1, max_length=32))],
    )
    description = ContractField(
        field_name=str(PublicAttrNamesEnum.description),
        nullable=False,
        use_cache=True,
    )

    @classmethod
    def create_new_passport_group(
        cls,
        *,
        name: str,
        description: str = "",
    ):
        return cls(
            id=None,
            name=name,
            description=description,
            created_at=None,
            updated_at=None,
        )

    def __init__(
        self,
        *,
        id: int | None,
        name: str,
        description: str,
        created_at: datetime | None,
        updated_at: datetime | None,
    ):
        super().__init__(id=id, created_at=created_at, updated_at=updated_at)
        self.description = description
        self.name = name


if __name__ == '__main__':
    pg = PassportGroupEntity.create_new_passport_group(
        name="test", description="test"
    )
    print(pg)