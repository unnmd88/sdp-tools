import re
from collections.abc import Sequence
from re import Pattern
from typing import Any

from domain.contracts.exc import ContractViolationFieldError
from domain.contracts.field_contracts.base import AbstractContractField
from domain.contracts.interfaces.cahe_interface import CacheFieldProtocol
from domain.contracts.interfaces.require_schemas_interfaces import (
    ContractProcessValueSchemaRequireProtocol,
    ContractRequireSchemaProtocol,
)


class ContractStringField(AbstractContractField):
    """Класс контракта строкового поля."""

    def __init__(
        self,
        *,
        field_name: str,
        min_length: int = None,
        max_length: int = None,
        pattern: str | Pattern = None,
        nullable: bool = False,
        pipeline_preprocess_value: Sequence[ContractProcessValueSchemaRequireProtocol]
        | None = None,
        pipeline_postprocess_value: Sequence[ContractProcessValueSchemaRequireProtocol]
        | None = None,
        requires: Sequence[ContractRequireSchemaProtocol] | None = None,
        invariants: Sequence[ContractRequireSchemaProtocol] | None = None,
        env_name: str | None = None,
        use_cache: bool = False,
        override_default_cache: CacheFieldProtocol | None = None,
    ):
        self._min_length = min_length
        self._max_length = max_length
        self._pattern = re.compile(pattern) if pattern is not None else pattern
        super().__init__(
            field_name=field_name,
            nullable=nullable,
            pipeline_preprocess_value=pipeline_preprocess_value,
            pipeline_postprocess_value=pipeline_postprocess_value,
            requires=requires,
            invariants=invariants,
            env_name=env_name,
            use_cache=use_cache,
            override_default_cache=override_default_cache,
        )

    def _validate(self, value: Any) -> Any:
        if self._min_length is not None and len(value) < self._min_length:
            err = f"Длина строки не может быть меньше {self._min_length} символов."
        elif self._max_length is not None and len(value) > self._max_length:
            err = f"Длина строки не может быть больше {self._max_length} символов."
        elif (self._pattern is not None) and (re.match(self._pattern, value) is None):
            err = "Строка не соответствует шаблону."
        else:
            err = None
        if err is not None:
            raise ContractViolationFieldError(
                field_name=self._name,
                value=value,
                context=f"Нарушен контракт строкового поля. {err}",
            )
        return super()._validate(value)

    def repr_schema(self):
        return (
            f"{super().repr_schema()} "
            f"min_length={self._min_length!r} "
            f"max_length={self._max_length!r}"
        )


if __name__ == "__main__":
    s1 = ContractStringField(
        min_length=1,
        max_length=100,
        pattern=r"[a-z]+",
        field_name="name",
        nullable=False,
        use_cache=True,
    )

    s2 = ContractStringField(
        min_length=1,
        max_length=100,
        pattern=r"[a-z]+",
        field_name="name",
        nullable=False,
        use_cache=True,
    )
    print(s1("tllofromfunc"))
    print(s1("tllofromfunc"))
    print(s2(1))
