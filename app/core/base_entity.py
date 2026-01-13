import json
from abc import ABC
from collections.abc import Generator
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from core.contracts.field_contracts.base import (
    ContractFieldId,
    ContractFieldCreatedAt,
    ContractFieldUpdatedAt,
)
from core.exceptions.contract import (
    ContractViolationPreConditionError,
)
from core.contracts.exc import ContractViolationInvariantError
from core.users.constants import MIN_ID, MAX_ID
from core.users.rules_messages import DomainRulesViolationsMessages


@dataclass(frozen=True, kw_only=True, slots=True)
class PublicAttr:
    attr_name: str
    alias: str | None = None


class AbstractEntity(ABC):
    time_format = "%Y-%m-%d %H:%M:%S"

    __public_attrs__ = (
        PublicAttr(attr_name="_id", alias="id"),
        PublicAttr(attr_name="_built_at", alias="built_at"),
        PublicAttr(attr_name="_updated_at", alias="updated_at"),
        PublicAttr(attr_name="_created_at", alias="created_at"),
    )

    contract_id = ContractFieldId(
        nullable=False,
        use_cache=True,
    )
    contract_created_at = ContractFieldCreatedAt(
        use_cache=False,
        nullable=True,
    )
    contract_updated_at = ContractFieldUpdatedAt(
        use_cache=False,
        nullable=True,
    )

    def __init__(
        self,
        *,
        id: int,
        created_at: datetime | None,
        updated_at: datetime | None,
    ):
        self._built_at = datetime.now()
        self._id = self.contract_id(id)
        self._created_at = self.contract_created_at(created_at)
        self._updated_at = self.contract_updated_at(updated_at)
        self.check_invariant_datetime()

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self._id == other.id
        raise NotImplementedError

    def __iter__(self) -> Generator[tuple[str, Any], None, None]:
        for attr in self.__public_attrs__:
            yield attr.alias, getattr(self, attr.attr_name)

    def __str__(self):
        attrs = " ".join(
            f"{attr}={value.strftime(self.time_format) if isinstance(value, datetime) else value}"
            for attr, value in self
        )
        return f"{self.__class__.__name__}({attrs})"

    def __repr__(self):
        attrs = " ".join(f"{attr}={value!r}" for attr, value in self)
        return f"{self.__class__.__name__}({attrs})"

    def to_dict(
        self,
        *,
        exclude: set[str] = None,
        include: dict = None,
    ) -> dict:
        d = {
            k: v.strftime(self.time_format) if isinstance(v, datetime) else v
            for k, v in self
        } | (include or {})
        for item in exclude or ():
            d.pop(item, None)
        return d

    def to_json(
        self,
        *,
        exclude: set[str] = None,
        include: dict = None,
        ensure_ascii: bool = True,
        indent: None | int | str = 2,
    ) -> str:
        return json.dumps(
            self.to_dict(exclude=exclude, include=include),
            ensure_ascii=ensure_ascii,
            indent=indent,
        )

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
        # В принципе можно эту проверку делать только при получении id из репозитория.
        if not MIN_ID <= id <= MAX_ID:
            raise ContractViolationPreConditionError(
                DomainRulesViolationsMessages.id_range
            )
        self._id = id
        return self._id

    def set_created_at(self, created_at: datetime | None) -> datetime | None:
        self._created_at = created_at
        self.check_invariant_datetime()
        return self._created_at

    def set_updated_at(self, updated_at: datetime | None) -> datetime | None:
        self._updated_at = updated_at
        self.check_invariant_datetime()
        return self._updated_at

    def check_invariant_datetime(self) -> None:
        """Проверка инвариантов даты и времени."""
        if self._created_at is not None:
            if self._updated_at is not None and self._created_at > self._updated_at:
                # TODO: добавить логирование!!
                raise ContractViolationInvariantError(
                    DomainRulesViolationsMessages.created_rule
                )
        if self._updated_at is not None:
            if self._created_at is not None and self._created_at > self._updated_at:
                # TODO: добавить логирование!!
                raise ContractViolationInvariantError(
                    DomainRulesViolationsMessages.updated_rule
                )


if __name__ == "__main__":
    o = AbstractEntity(id=1, created_at=None, updated_at=None)
    print(o.id)
    print(list(o))
    print(list(o))
