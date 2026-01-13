from types import UnionType


class ContractViolationError(Exception):
    """Базовый класс для исключений, возникающих при нарушении контракта."""


class ContractViolationPreProcessingError(ContractViolationError):
    """Класс исключений, возникающих при нарушении контракта предобработки."""


class ContractViolationValueTypeError(ContractViolationError):
    """Ошибка нарушения типа значения."""

    def __init__(
        self,
        *,
        arg_name: str,
        got: type | None,
        expected: str | type | tuple[str | type, ...] | UnionType,
    ):
        self._detail = (
            f"Нарушен контракт типа данных для {arg_name!r}."
            f" Значение={got!r}({got.__class__!r}). Ожидается {str(expected)!r}."
        )
        super().__init__(self._detail)

    @property
    def detail(self):
        return self._detail


class ContractViolationBusinessRulesError(ContractViolationError):
    """Ошибка нарушения контракта бизнес-правил."""


class ContractViolationReturnValueError(ContractViolationError):
    """Ошибка нарушения контракта возвращаемого значения."""


class ContractViolationInvariantError(ContractViolationError):
    """Ошибка нарушения типа значения."""


class ContractViolationHasNoPermissionError(ContractViolationError):
    """Ошибка нарушения прав доступа."""
