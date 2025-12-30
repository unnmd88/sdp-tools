from typing import Protocol, TypeVar, ClassVar

TM = TypeVar('TM')
TE = TypeVar('TE')


class BaseDBMapperProtocol(Protocol):

    entity: ClassVar

    @classmethod
    def to_entity(cls, db_model: TM) -> TE: ...

    def to_model(self, entity: TE) -> TM: ...

    @classmethod
    def entity_validate(cls, **fields, ):
        """ Проверка корректности полей путём создания модели. """
        return cls.entity(**fields)


