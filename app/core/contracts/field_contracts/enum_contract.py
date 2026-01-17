from enum import StrEnum, Enum
from typing import Sequence, Any

from core.contracts.exc import ContractViolationFieldError
from core.contracts.field_contracts.base import AbstractContractField
from core.contracts.interfaces.cahe_interface import CacheFieldProtocol
from core.contracts.interfaces.require_schemas_interfaces import (
    ContractProcessValueSchemaRequireProtocol,
    ContractRequireSchemaProtocol,
)
from core.contracts.require_schemas import ContractProcessValueRequireSchema
from core.contracts.utils import replace_self_from_attr_name


class ContactEnumField(AbstractContractField):
    """Класс для создания контракта поля типа Enum."""

    violation_pattern = "Значение {} не входит в перечисление {}."

    def __init__(
        self,
        *,
        field_name: str,
        enum: type[Enum],
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
    ) -> None:
        self._enum = enum
        if not isinstance(self._enum, type) and not issubclass(enum, Enum):
            raise TypeError(
                "Аргумент {} должен быть подклассом Enum".format(
                    replace_self_from_attr_name(f"{self._enum=}")
                ),
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
            override_default_cache=override_default_cache,
        )

    def repr_schema(self):
        return f"{super().repr_schema()} enum={self._enum!r}"

    def _validate(self, value: Any) -> Any:
        try:
            value = self._enum(value)
        except ValueError:
            raise ContractViolationFieldError(
                contract="Enum",
                violation=self.violation_pattern.format(value, self._enum),
                field_name=self._name,
                value=value,
                detail=f"Нарушен контракт принадлежности значения {value!r} к перечислению Enum: {self._enum.__name__!r}",
            )
        return super()._validate(value)


if __name__ == "__main__":

    class En(StrEnum):
        DEV = "Dev"
        TEST = "test"
        PROD = "prod"

    _enum = ContactEnumField(
        enum=En,
        field_name="test_enum",
        nullable=False,
        pipeline_preprocess_value=[
            ContractProcessValueRequireSchema(handler=lambda x: x.capitalize())
        ],
    )
    print(_enum("DEV"))
    print(repr(_enum))
