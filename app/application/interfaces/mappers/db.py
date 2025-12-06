from typing import Protocol, TypeVar

TM = TypeVar('TM')
TE = TypeVar('TE')


class BaseDBMapperProtocol(Protocol):
    @classmethod
    def to_entity(cls, db_model: TM) -> TE: ...

    def to_model(self, entity: TE) -> TM: ...
