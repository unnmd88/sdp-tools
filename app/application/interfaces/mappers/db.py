from typing import Protocol, TypeVar


TM = TypeVar("TM")
TE = TypeVar("TE")


class BaseDBMapperProtocol(Protocol[TM, TE]):
    @classmethod
    def to_entity(cls, db_model: TM) -> TE: ...

    @classmethod
    def to_model(cls, entity: TE) -> TM: ...

    @classmethod
    def update_model(cls, *, model: TM, entity: TE) -> TM: ...
