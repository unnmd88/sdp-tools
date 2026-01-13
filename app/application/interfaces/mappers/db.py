from typing import Protocol, TypeVar, ClassVar, Any


TM = TypeVar("TM")
TE = TypeVar("TE")


def abstactmethod(args):
    pass


class BaseDBMapperProtocol(Protocol):
    entity: ClassVar

    @classmethod
    @abstactmethod
    def fields_validate(cls, **fields: Any) -> bool: ...

    @classmethod
    def to_entity(cls, db_model: TM) -> TE: ...

    def to_model(self, entity: TE) -> TM: ...

    @classmethod
    def entity_validate(
        cls,
        **fields,
    ):
        """Проверка корректности полей путём создания модели."""
        return cls.entity(**fields)
