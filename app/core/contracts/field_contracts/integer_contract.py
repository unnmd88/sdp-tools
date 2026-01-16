from collections.abc import Sequence
from typing import Any

from core.contracts.exc import ContractViolationFieldError
from core.contracts.field_contracts.base import AbstractContractField
from core.contracts.interfaces.require import ContractProcessValueRequireProtocol, ContractRequireProtocol

from core.contracts.requires import ContractRequire, ContractProcessValueRequire


class ContractIntegerField(AbstractContractField):
    """ Класс для создания контракта целочисленного поля. """

    def __init__(
        self,
        *,
        field_name: str,
        nullable: bool = False,
        pipeline_preprocess_value: Sequence[ContractProcessValueRequireProtocol] | None = None,
        pipeline_postprocess_value: Sequence[ContractProcessValueRequireProtocol] | None = None,
        requires: Sequence[ContractRequireProtocol] | None = None,
        invariants: Sequence[ContractRequireProtocol] | None = None,
        env_name: str | None = None,
        use_cache: bool = False,
        min_value: int = 0,
        max_value: int | None = None,
    ):
        self._min_value = min_value
        self._max_value = max_value
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

    def repr_schema(self):
        return (
            f"{super().repr_schema()} "
            f"min_value={self._min_value!r} "
            f"max_value={self._max_value!r} "
        )

    def _validate(self, value: Any) -> Any:
        err = None
        if value < self._min_value:
            err = f"Значение {value} меньше минимального {self._min_value}."
        elif value > self._max_value:
            err = f"Значение {value} больше максимального {self._max_value}."

        if err is not None:
            err_pattern = "Диапазон допустимых значений целого числа: от {} до {}"
            raise ContractViolationFieldError(
                contract=err_pattern.format(self._min_value, self._max_value),
                field_name=self._name,
                violation=err,
                value=value,
                detail="Нарушен контракт диапазона допустимых значений целого числа: от {} до {}. {}".format(
                    self._min_value, self._max_value, err
                ),
            )
        return super()._validate(value)


if __name__ == '__main__':
    pos_int = ContractIntegerField(
        field_name="test2",
        min_value=0,
        max_value=1000,
        nullable=False,
        pipeline_preprocess_value=[
            ContractProcessValueRequire(handler=int),
        ],
        invariants=[ContractRequire(handler=lambda x: x <= 450, contract="test", violation="test", detail="Значение не должно быть больше 450")],
        use_cache=True,
    )
    print(pos_int(4))
    print(pos_int(5))
    print(pos_int("10"))
    print(pos_int.get_cache())
    print(repr(pos_int))

