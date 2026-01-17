import json
from abc import ABC, abstractmethod
from collections.abc import Generator
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Self

from core.contracts.exc import ContractViolationInvariantError
from core.contracts.field_contracts.datetime_contract import ContractDateTimeField
from core.contracts.field_contracts.integer_contract import ContractIntegerField


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

    _contract_id = ContractIntegerField(
        field_name="id",
        nullable=False,
        use_cache=True,
    )
    _contract_created_at = ContractDateTimeField(
        field_name="created_at",
        use_cache=False,
        nullable=True,
    )
    _contract_updated_at = ContractDateTimeField(
        field_name="updated_at",
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
        self._id = id
        self._created_at = created_at
        self._updated_at = updated_at
        self.check_invariant_datetime()

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self._id == other.id
        raise NotImplementedError

    def __iter__(self) -> Generator[Any, None, None]:
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

    @classmethod
    @abstractmethod
    def validate(cls, **kwargs) -> Self: ...

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

    def check_invariant_datetime(self) -> None:
        """Проверка инвариантов даты и времени."""
        if self._created_at is not None:
            if self._updated_at is not None and self._created_at > self._updated_at:
                # TODO: добавить логирование!!
                raise ContractViolationInvariantError
        if self._updated_at is not None:
            if self._created_at is not None and self._created_at > self._updated_at:
                # TODO: добавить логирование!!
                raise ContractViolationInvariantError
