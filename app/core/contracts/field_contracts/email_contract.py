import re
from collections.abc import Sequence
from re import Pattern
from typing import Any

from core.contracts.exc import ContractViolationFieldError
from core.contracts.field_contracts.base import AbstractContractField
from core.contracts.interfaces.require_schemas_interfaces import (
    ContractProcessValueSchemaRequireProtocol,
    ContractRequireSchemaProtocol,
)


DEFAULT_EMAIL_PATTERN = re.compile(r"^\S+@\S+\.\S+$")


class ContractEmailField(AbstractContractField):
    """Класс контракта строкового поля."""

    def __init__(
        self,
        *,
        pattern: str | Pattern = DEFAULT_EMAIL_PATTERN,
        field_name: str,
        nullable: bool = False,
        pipeline_preprocess_value: Sequence[ContractProcessValueSchemaRequireProtocol]
        | None = None,
        pipeline_postprocess_value: Sequence[ContractProcessValueSchemaRequireProtocol]
        | None = None,
        requires: Sequence[ContractRequireSchemaProtocol] | None = None,
        invariants: Sequence[ContractRequireSchemaProtocol] | None = None,
        env_name: str | None = None,
        use_cache: bool = False,
    ):
        self._pattern = re.compile(
            pattern if pattern is not None else DEFAULT_EMAIL_PATTERN
        )
        super().__init__(
            field_name=field_name,
            nullable=nullable,
            pipeline_preprocess_value=pipeline_preprocess_value,
            pipeline_postprocess_value=pipeline_postprocess_value,
            requires=requires,
            invariants=invariants,
            env_name=env_name,
            use_cache=use_cache,
        )

    def _validate(self, value: Any) -> Any:
        if re.match(pattern=self._pattern, string=value) is None:
            raise ContractViolationFieldError(
                contract="Требования 'email' поля",
                field_name=self._name,
                violation="Некорректный формат email",
                value=value,
                detail="Нарушен контракт поля, содержащего 'email'",
            )

        return super()._validate(value)


if __name__ == "__main__":
    s = ContractEmailField(
        field_name="name",
        nullable=False,
    )

    print(s("jurek@mail.ru"))
