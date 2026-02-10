from dataclasses import dataclass


@dataclass(slots=True, kw_only=True, frozen=True)
class TypeControllerVO:
    value: str