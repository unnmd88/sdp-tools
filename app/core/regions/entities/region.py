from dataclasses import dataclass
from typing import ClassVar

from core.constants import ALLOWED_REGIONS
from core.enums import RegionCodes, RegionNames
from core.users.exceptions import DomainValidationError

T_ALLOWED_REGIONS = frozenset[tuple[RegionNames, RegionCodes]]


@dataclass(frozen=True, slots=True, kw_only=True)
class RegionEntity:

    allowed_regions: ClassVar[T_ALLOWED_REGIONS] = ALLOWED_REGIONS

    code: int
    name: str
    id: int | None = None

    def __eq__(self, other):
         if not isinstance(other, RegionEntity):
             return NotImplemented
         return self.code == other.code and self.name == other.name

    # def __post_init__(self):
    #     if (self.name, self.code) not in self.allowed_regions:
    #         raise DomainValidationError('Недопустимая пара кода и названия для региона')

