from dataclasses import dataclass
from typing import Any


@dataclass(slots=True, frozen=True)
class BaseVoBuilder[T_V, T_VO]:
    vo_class: type[T_VO]

    def __call__(self, value: T_V) -> T_VO:
        return self.vo_class(value)

    @classmethod
    def build_from_value(cls, vo: type[T_VO], value: T_V) -> T_VO:
        return cls(vo_class=vo)(value)

    def is_vo_instance(self, value: Any) -> bool:
        return isinstance(value, self.vo_class)