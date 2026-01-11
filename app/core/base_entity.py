import json
from abc import ABC, abstractmethod
from datetime import datetime

from core.exceptions.contract import (
    ContractViolationPreConditionError,
    ContractViolationValueTypeError,
    ContractViolationInvariantError
)
from core.users.constants import MIN_ID, MAX_ID
from core.users.rules_messages import DomainRulesViolationsMessages


class AbstractEntity(ABC):

    time_format = '%Y-%m-%d %H:%M:%S'

    def __init__(
        self,
        *,
        id: int,
        created_at: datetime | None,
        updated_at: datetime | None,
    ):
        self._built_at = datetime.now()
        self._id = self.set_id(id)
        self._created_at = self.set_created_at(created_at)
        self._updated_at = self.set_updated_at(updated_at)
        self.check_invariant_datetime()

    @abstractmethod
    def to_dict(self) -> dict:
        ...

    def to_json(
        self,
        *,
        ensure_ascii: bool = True,
        indent: None | int | str = 2,
    ) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=ensure_ascii, indent=indent)

    @property
    def built_at(self) -> datetime:
        return self._built_at

    @property
    def id(self) -> int | None:
        return self._id

    @property
    def created_at(self) -> datetime | None:
        return self._created_at

    @property
    def updated_at(self) -> datetime | None:
        return self._updated_at

    def set_id(self, id: int) -> int:
        if not isinstance(id, int):
            # TODO: добавить логирование!!
            raise ContractViolationValueTypeError(DomainRulesViolationsMessages.id_isinstance)
        if not MIN_ID <= id <= MAX_ID:
            raise ContractViolationPreConditionError(DomainRulesViolationsMessages.id_range)
        self._id = id
        return self._id

    def set_created_at(self, created_at: datetime | None) -> datetime | None:
        if created_at is None:
            self._created_at = created_at
            return self._created_at
        if not isinstance(created_at, datetime):
            raise ContractViolationValueTypeError(DomainRulesViolationsMessages.created_at_isinstance)
        self._created_at = created_at
        return self._created_at

    def set_updated_at(self, updated_at: datetime | None) -> datetime | None:
        if updated_at is None:
            self._updated_at = updated_at
            return self._updated_at
        if not isinstance(updated_at, datetime):
            raise ContractViolationValueTypeError(DomainRulesViolationsMessages.updated_at_isinstance)
        self._updated_at = updated_at
        return self._updated_at

    def check_invariant_datetime(self) -> None:
        """ Проверка инвариантов даты и времени. """
        if self._created_at is not None:
            if self._updated_at is not None and self._created_at > self._updated_at:
                # TODO: добавить логирование!!
                raise ContractViolationInvariantError(DomainRulesViolationsMessages.created_rule)
        if self._updated_at is not None:
            if self._created_at is not None and self._created_at > self._updated_at:
                # TODO: добавить логирование!!
                raise ContractViolationInvariantError(DomainRulesViolationsMessages.updated_rule)


if __name__ == '__main__':

    o = AbstractEntity(id=1, created_at=None, updated_at=None)
    print(o.id)

