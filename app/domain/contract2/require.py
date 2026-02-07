from dataclasses import dataclass
from typing import Callable


@dataclass(kw_only=True, frozen=True, slots=True)
class Require:
    handler: Callable
    contract: str | None = None
    violation: str | None = None
    message: str | None = None
