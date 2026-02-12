from dataclasses import dataclass
from typing import final


@final
@dataclass(frozen=True, kw_only=True, slots=True)
class NullableConfig:
    """Конфигурация nullable поведения."""
    allow_none: bool = False
    public_message: str
