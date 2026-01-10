from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True, kw_only=True)
class BaseEntityMixin:

    id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

