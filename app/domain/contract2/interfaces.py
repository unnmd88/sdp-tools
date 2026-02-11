from typing import runtime_checkable, Protocol, Any


@runtime_checkable
class BuilderProtocol[T_Primitive, T_VO](Protocol):
    def __call__(self, value: T_Primitive) -> T_VO: ...
    def is_vo_instance(self, value: Any) -> bool: ...