from datetime import datetime

from core.services.contract import contract, ContractConditions
from core.users.constants import MIN_ID, MAX_ID
from core.users.exceptions import DominTypeValidationError, DomainValidationError

_ID_MSG = f'id должен быть в диапазоне от {MIN_ID} до {MAX_ID} или None'


class BaseEntity:

    def __init__(
        self,
        *,
        entity_id: int | None,
        created_at: datetime | None,
        updated_at: datetime | None,
    ):
        self._built_at = datetime.now()
        self._id = self._validate_id(entity_id)
        self._created_at = self._validate_created_at(created_at)
        self._updated_at = self._validate_updated_at(updated_at)

    @property
    def entity_id(self) -> int | None:
        return self._id

    @property
    def built_at(self) -> datetime:
        return self._built_at

    @property
    def created_at(self) -> datetime | None:
        return self._created_at

    @property
    def updated_at(self) -> datetime | None:
        return self._updated_at

    @contract(
        type_check=int | None,
        preconditions=ContractConditions(
            requires=[
                    (lambda x: x is None or (MIN_ID <= x <= MAX_ID), _ID_MSG),
                ],
            exception=DomainValidationError
        ),
        field_name="id",
    )
    def _validate_id(self, id: int | None) -> int | None:
        assert isinstance(id, int | None)
        assert id is not None and MIN_ID <= id <= MAX_ID
        return id

    @contract(
        type_check=datetime | None,
        field_name="created_at",
    )
    def _validate_created_at(self, date_time: datetime | None) -> datetime | None:
        assert self._built_at > date_time if date_time else date_time is None
        return date_time

    @contract(
        type_check=datetime | None,
        field_name="updated_at",
    )
    def _validate_updated_at(self, date_time: datetime | None) -> datetime | None:
        assert self._built_at > date_time if date_time else date_time is None
        return date_time


if __name__ == '__main__':
    print(int | None)
    print(str(int | None).replace('|', 'или'))
    o = BaseEntity(1, datetime.now(), None)
    print(o.get_id())
    print(o.built_at)
