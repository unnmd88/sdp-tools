from dataclasses import dataclass

from core.enums import RegionCodes, RegionNames
from core.field_validators import check_is_valid_enum


@dataclass
class Region:
    id: int
    code: RegionCodes
    name: RegionNames

    def __post_init__(self):
        check_is_valid_enum(RegionCodes, self.code)
        check_is_valid_enum(RegionNames, self.name)
