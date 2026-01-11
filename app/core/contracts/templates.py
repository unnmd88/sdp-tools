from dataclasses import dataclass
from typing import Callable

from core.exceptions.contract import (
    ContractViolationError,
    ContractViolationValueTypeError,
)


@dataclass(kw_only=True, frozen=True, slots=True)
class ContractRequire:
    """
    Контейнер для предусловий валидации значения в контракте.

    Используется для определения предусловий, которые должны быть выполнены
    при проверке корректности значения (например, в валидаторах доменных объектов).
    В случае, если одно из условий не выполняется, выбрасывается указанное исключение
    с соответствующим сообщением об ошибке.
    Args
        predicate: Callable[..., bool] | Callable[[], bool]
        exception: ContractViolationError = ContractViolationError
    """

    predicate: Callable[..., bool] | Callable[[], bool]
    exception: ContractViolationError | type[ContractViolationError] = (
        ContractViolationError
    )

    def __iter__(self):
        return (el for el in (self.predicate, self.exception))

    def __post_init__(self):
        if not callable(self.predicate):
            raise TypeError('predicate должен быть функцией')
        if isinstance(self.exception, type):
            if not issubclass(
                self.exception, ContractViolationValueTypeError | ContractViolationError
            ):
                raise TypeError(
                    f'Некорректный exception: {self.exception}. '
                    f'Должен быть подклассом {ContractViolationError.__name__}'
                )
        elif not isinstance(self.exception, ContractViolationError):
            raise TypeError(
                f'Некорректный exception: {self.exception}. '
                f'Должен быть экземпляром {ContractViolationError.__name__} или его потомка'
            )
