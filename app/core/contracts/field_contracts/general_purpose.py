from datetime import datetime
from enum import Enum, StrEnum

from core.contracts.field_contracts import ContractField
from core.contracts.requires import ContractRequire


class ContractIdPositiveIntegerField(ContractField):
    expected_types = int
    base_requires = (
        ContractRequire(
            predicate=lambda value: value > 0,
            detail="Значение должно быть целым положительным числом больше нуля.",
        ),
    )


class ContractDateField(ContractField):
    expected_types = datetime

class E(Enum):
    fidrt = 1
    f= 2

class S(StrEnum):
    forst = 'forst'

class ContractRoleField(ContractEnumField):
    expected_types = E



if __name__ == "__main__":
    ob = ContractIdPositiveIntegerField(
        field_name="id",
        nullable=False,
        use_cache=True,
    )
    print(ob)
    print(ob(123))
    print(ob(2))

    ob2 = ContractDateField(
        field_name="created_at",
        nullable=True,
        use_cache=False,
    )

    ob3 = ContractField(
        field_name="role",
        nullable=False,
        use_cache=True,
        override_self_expected_types=E,
    )
    print(ob3(1))
    print(ob3)

    ob4 = ContractRoleField(
        field_name="role",
        nullable=False,
        use_cache=True,

    )

    print(ob4)
    print(ob4(2))