from dataclasses import dataclass
from typing import Any


@dataclass(slots=True, frozen=True, kw_only=True)
class FiltersFactory:
    @classmethod
    def get_filters_dict(
        cls,
        *,
        code: int | None = None,
        name: str | None = None,
    ) -> dict[str, Any]:
        filters = {}
        if code is not None:
            filters["code"] = code
        if name is not None:
            filters["name"] = name
        return filters
