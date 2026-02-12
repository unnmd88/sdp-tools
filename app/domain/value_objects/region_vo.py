from dataclasses import dataclass

from domain.kernel.enums.attrs_names import PublicAttrNamesEnum
from domain.kernel.primitives.integer_validator import IntegerValidator


@dataclass(slots=True, kw_only=True, frozen=True)
class RegionVo:
    code: int
    name: str


@dataclass(slots=True, frozen=True)
class RegionCodeVo:
    value: int

    def __post_init__(self):
        (IntegerValidator(self.value)
        .ensure_positive()
        .ensure_gt(1)
         )
