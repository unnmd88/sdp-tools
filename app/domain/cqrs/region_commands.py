from dataclasses import dataclass
from typing import ClassVar

from domain.enums.keep_value_enum import Keep


@dataclass(slots=True, kw_only=True, frozen=True)
class UpdateRegionCommand:
    operation_name: ClassVar[str] = "Обновить регион"
    customer_id: int
    code_or_name: str

    new_code: int | Keep = Keep.VALUE
    new_name: str | Keep = Keep.VALUE


@dataclass(slots=True, kw_only=True, frozen=True)
class CreateRegionCommand:
    operation_name: ClassVar[str] = "Создать регион"
    customer_id: int

    code: int
    name: str


@dataclass(slots=True, kw_only=True, frozen=True)
class DeleteRegionCommand:
    operation_name: ClassVar[str] = "Удалить регион"
    customer_id: int

    code_or_name: str
