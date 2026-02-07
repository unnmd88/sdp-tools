from dataclasses import dataclass

from domain.enums.keep_value_enum import Keep


@dataclass(slots=True, kw_only=True, frozen=True)
class UpdatePassportGroupCommand:
    customer_id: int
    name: str

    new_name: str | Keep = Keep.VALUE
    new_description: str | Keep = Keep.VALUE


@dataclass(slots=True, kw_only=True, frozen=True)
class CreatePassportGroupCommand:
    customer_id: int

    name: str
    description: str


@dataclass(slots=True, kw_only=True, frozen=True)
class DeletePassportGroupCommand:
    customer_id: int

    name: str