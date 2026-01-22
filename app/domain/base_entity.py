import json
from abc import ABC
from collections.abc import Generator
from datetime import datetime
from typing import Any

from domain.contract2.contract_field import ContractField
from domain.contract2.require import Require
from domain.contracts.exc import ContractViolationInvariantError
from domain.entities_public_attrs import PublicAttr, BASE_PUBLIC_ATTRS
from domain.validators.general_purpose import GeneralPurposeValidator


class AbstractEntity(ABC):
    time_format = "%Y-%m-%d %H:%M:%S"

    __public_attrs__ = BASE_PUBLIC_ATTRS

    id = ContractField(
        field_name="id",
        nullable=True,
        use_cache=False,
        requires=[Require(handler=GeneralPurposeValidator.pk_id)]
    )

    # _contract_id = ContractIntegerField(
    #     field_name="id",
    #     nullable=True,
    #     use_cache=True,
    # )
    # _contract_created_at = ContractDateTimeField(
    #     field_name="created_at",
    #     use_cache=False,
    #     nullable=True,
    # )
    # _contract_updated_at = ContractDateTimeField(
    #     field_name="updated_at",
    #     use_cache=False,
    #     nullable=True,
    # )

    def __init__(
        self,
        *,
        id: int | None,
        created_at: datetime | None,
        updated_at: datetime | None,
    ):
        self._built_at = datetime.now()
        self.id = id
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

    def to_dict(
        self,
        *,
        exclude: set[str] = None,
        **include,
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
