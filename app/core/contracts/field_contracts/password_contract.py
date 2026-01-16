from collections.abc import Sequence

from core.contracts.exc import ContractViolationFieldError
from core.contracts.field_contracts.base import AbstractContractField
from core.contracts.interfaces.require_schemas_interfaces import (
    ContractProcessValueSchemaRequireProtocol,
    ContractRequireSchemaProtocol,
)


class ContractHashedPasswordField(AbstractContractField):
    """Класс контракта поля, содержащего пароль."""

    def __init__(
        self,
        *,
        field_name: str,
        pipeline_preprocess_value: Sequence[ContractProcessValueSchemaRequireProtocol]
        | None = None,
        pipeline_postprocess_value: Sequence[ContractProcessValueSchemaRequireProtocol]
        | None = None,
        requires: Sequence[ContractRequireSchemaProtocol] | None = None,
        invariants: Sequence[ContractRequireSchemaProtocol] | None = None,
        env_name: str | None = None,
        use_cache: bool = False,
    ):
        self._field_name = field_name
        super().__init__(
            field_name=field_name,
            nullable=False,
            pipeline_preprocess_value=pipeline_preprocess_value,
            pipeline_postprocess_value=pipeline_postprocess_value,
            requires=requires,
            invariants=invariants,
            env_name=env_name,
            use_cache=use_cache,
        )

    def _check_value_type(self, value: bytes) -> None:
        if not isinstance(value, bytes):
            err = f"Значение пароля должно быть типа {bytes.__name__!r}."
        elif len(value) <= 1:
            err = f"Количество символов в пароле должно быть больше 1. Текущее={len(value)}."
        else:
            err = None
        if err is not None:
            raise ContractViolationFieldError(
                contract="Требования поля пароля",
                field_name=self._name,
                violation=err,
                value=value,
                detail=f"Нарушен контракт поля, содержащего пароль. {err}",
            )

    def _validate(self, value: bytes) -> bytes:
        self._check_value_type(value)
        value = super()._validate(value)
        self._check_value_type(value)
        return value


if __name__ == "__main__":
    s = ContractHashedPasswordField(
        field_name="password",
    )
    print(s(b"t"))
