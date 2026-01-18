from typing import Protocol, Any, TypeVar

T_Entity = TypeVar("T_Entity")


class EntityFactoryServiceProtocol(Protocol[T_Entity]):
    @classmethod
    def create_existing(cls, **kwargs) -> T_Entity: ...
    @classmethod
    def create_new(cls, **kwargs) -> T_Entity: ...
