from dataclasses import dataclass
from typing import Any


@dataclass(kw_only=True, slots=True, frozen=True)
class TokenErrorContextVO:
    subject: Any = None
    handler: str | None = None
    token_type: str | None = None
    expected_token_type: str | None = None
    token: str | None = None
    message: str | None = None
    internal_message: str | None = None
