from dataclasses import dataclass

from domain.enums.keep_value_enum import Keep


@dataclass(slots=True, kw_only=True, frozen=True)
class UpdateRegionCommand:
    user_id: int
    code_or_name: str | int

    new_code: int | Keep = Keep.VALUE
    new_name: str | Keep = Keep.VALUE



