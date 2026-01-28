from dataclasses import dataclass
from enum import StrEnum
from types import UnionType
from typing import Any


@dataclass(kw_only=True, slots=True, frozen=True)
class ApplicationErrorContextVO:
    use_case: str | None = None
    service: str | None = None
    handler: str | None = None
    reason: str | None = None
    rule: str | None = None
    internal_message: str | None = None
    message: str | None = None

