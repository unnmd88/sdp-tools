from typing import Protocol, TypeVar


TM = TypeVar("TM")
TE = TypeVar("TE")


class BaseDBMapperProtocol(Protocol):
    @classmethod
    def to_entity(cls, db_model: TM) -> TE: ...

    @classmethod
    def to_model(cls, entity: TE) -> TM: ...
