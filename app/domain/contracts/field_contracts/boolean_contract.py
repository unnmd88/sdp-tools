from typing import Any

from domain.contracts.exc import ContractViolationFieldError
from domain.contracts.field_contracts.base import AbstractContractField


class ContractBooleanField(AbstractContractField):
    """Класс контракта поля, содержащего пароль."""

    def __init__(
        self,
        *,
        field_name: str,
        nullable: bool = False,
        allow_1_and_0_as_true_and_false: bool = True,
        env_name: str | None = None,
        use_cache: bool = False,
    ):
        self._field_name = field_name
        self._allow_1_and_0_as_true_and_false = allow_1_and_0_as_true_and_false
        if self._allow_1_and_0_as_true_and_false:
            self._convert_to_bool_type_or_identity = bool
        else:
            self._convert_to_bool_type_or_identity = lambda x: x
        self._env = env_name
        self._use_cache = use_cache
        super().__init__(
            field_name=field_name,
            nullable=nullable,
            env_name=env_name,
            use_cache=use_cache,
        )

    def __call__(self, value: Any) -> bool | None:
        if value is None:
            if self._nullable:
                self._check_invariants(value)
                return None
            raise ContractViolationFieldError(
                field_name=self._name,
                contract=f"'nullable'={self._nullable!r}",
                violation=f"Значение поля не может быть {None!r}",
                value=value,
            )
        value = self._convert_to_bool_type_or_identity(value)
        if not isinstance(value, bool):
            err = f"Значение должно быть типа {bool.__name__!r}."
            raise ContractViolationFieldError(
                contract="Требования поля булевого типа",
                field_name=self._name,
                violation=err,
                value=value,
                detail=err,
            )
        assert isinstance(value, bool), "Дольше должно быть bool"
        return value

    def repr_schema(self):
        return (
            f"{super().repr_schema()} "
            f"allow_1_and_0_as_true_and_false={self._allow_1_and_0_as_true_and_false!r} "
        )


if __name__ == "__main__":
    s = ContractBooleanField(
        field_name="is_active",
    )
    print(s(2))
