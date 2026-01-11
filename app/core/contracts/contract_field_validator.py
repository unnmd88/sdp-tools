from collections.abc import Callable, Iterable
from dataclasses import dataclass
from enum import IntEnum
from typing import Any, ClassVar

from core.exceptions.contract import (
    ContractViolationValueTypeError,
    ContractViolationPreConditionError,
)
from core.contracts.templates import ContractRequire


class ValidationLevels(IntEnum):
    strict = 60
    light = 50


@dataclass(kw_only=True, frozen=True, slots=True)
class FieldValidatorContract:
    # TODO: Добавить логирование

    default_err_message: ClassVar[str] = 'Неверный тип данных для поля'

    name: str
    nullable: bool
    before_validators: Callable[..., Any] = lambda x: x  # Identity по умолчанию
    validators: Iterable[ContractRequire] = ()
    repair: Callable[..., Any] = lambda x: x
    level: ValidationLevels = ValidationLevels.strict
    expected_type_message: str = ''

    def __post_init__(self):
        if not isinstance(self.name, str):
            raise TypeError('Имя поля должно быть строкой')
        if not callable(self.before_validators):
            raise TypeError('Предусловие должно быть callable-объектом')
        if not isinstance(self.nullable, bool):
            raise TypeError('Nullable должно быть булевым значением')
        if any(
            not isinstance(predicate, ContractRequire) for predicate in self.validators
        ):
            raise TypeError(
                f'Валидаторы должны быть итерируемыми объектами типа {ContractRequire.__name__!r}'
            )
        try:
            ValidationLevels(self.level)
        except ValueError:
            raise TypeError(
                f"Неверное значение для поля 'mode'. Допустимы из класса {ValidationLevels.__name__!r}"
            )

    def __call__(self, value: Any) -> Any:
        try:
            value = self.before_validators(value)
        except Exception:
            raise ContractViolationPreConditionError
        if value is None and self.nullable:
            return None
        for predicate, exception in self.validators:
            if not predicate(value):
                exc = None
                if self.level < ValidationLevels.strict:
                    if repaired_value := self.repair(value):
                        value = repaired_value
                    else:
                        exc = exception
                else:
                    exc = exception
                if exc is not None:
                    if isinstance(exc, type) and issubclass(
                        exc, ContractViolationValueTypeError
                    ):
                        raise ContractViolationValueTypeError(
                            arg_name=self.name,
                            got=value,
                            expected=self.expected_type_message,
                        )
                    raise exc
        return value


if __name__ == '__main__':
    o = FieldValidatorContract(
        name='test',
        # before_validators=lambda x: int(x),
        nullable=False,
        validators=[
            ContractRequire(
                predicate=lambda x: isinstance(x, int),
                exception=ContractViolationValueTypeError('Неверный тип данных'),
            ),
            ContractRequire(
                predicate=lambda x: x > 0,
                exception=ContractViolationValueTypeError('Неверное значение'),
            ),
        ],
        repair=lambda x: int(x) if isinstance(x, str) and x.strip().isdigit() else x,
        level=ValidationLevels.strict,
    )
    o(1)
    o('1')
