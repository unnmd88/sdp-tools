import re
from dataclasses import dataclass
from enum import StrEnum
from types import UnionType
from typing import Any


@dataclass(kw_only=True, slots=True, frozen=True)
class ContractViolationContextVO:
    contract_code: str | None = None
    subject: Any = None
    validator_class: str = None
    handler: str | None = None
    field_name: str | None = None
    value: Any = None
    violation: str | StrEnum = None
    rule: str | None = None
    message: str | None = None
    expected_type: type | UnionType | tuple[type] = None
    expected_pattern: str | re.Pattern | None = None

    @property
    def verbose_handler(self) -> str:
        return f"class={self.validator_class!r} : method={self.handler!r}"



