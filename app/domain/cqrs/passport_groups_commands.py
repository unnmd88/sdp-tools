from dataclasses import dataclass
from typing import ClassVar

from domain.enums.keep_value_enum import Keep


@dataclass(slots=True, kw_only=True, frozen=True)
class UpdatePassportGroupCommand:
    operation_name: ClassVar[str] = "Удалить группу паспортов"
    customer_id: int
    name: str

    new_name: str | Keep = Keep.VALUE
    new_description: str | Keep = Keep.VALUE


@dataclass(slots=True, kw_only=True, frozen=True)
class CreatePassportGroupCommand:
    operation_name: ClassVar[str] = "Создать новую группу паспортов"

    customer_id: int

    name: str
    description: str


@dataclass(slots=True, kw_only=True, frozen=True)
class DeletePassportGroupCommand:
    operation_name: ClassVar[str] = "Обновить группу паспортов"
    customer_id: int

    name: str
