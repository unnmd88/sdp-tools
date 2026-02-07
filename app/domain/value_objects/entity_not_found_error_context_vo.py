from dataclasses import dataclass
from enum import StrEnum
from types import UnionType
from typing import Any


@dataclass(kw_only=True, slots=True, frozen=True)
class EntityNotFoundErrorContextVO:
    entity: Any = None
    search_criteria: Any = None
    message: str | None = None
