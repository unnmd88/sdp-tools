from core.exceptions.base import DomainValidationError


class ContractViolationError(DomainValidationError):
    """Ошибка нарушения контракта."""


class ContractViolationValueTypeError(ContractViolationError):
    """Ошибка нарушения типа значения."""

    def __init__(
        self,
        *,
        arg_name: str,
        got: type,
        expected: str,
    ):
        self._detail = f'Неверный тип данных для {arg_name!r}: {got.__class__.__name__!r}. Ожидается {expected!r}.'
        super().__init__(self._detail)

    @property
    def detail(self):
        return self._detail


class ContractViolationBusinessRulesError(ContractViolationError):
    """Ошибка нарушения контракта бизнес-правил."""


class ContractViolationPreConditionError(ContractViolationError):
    """Ошибка нарушения контракта предусловия."""


class ContractViolationPostConditionError(ContractViolationError):
    """Ошибка нарушения контракта постусловия."""


class ContractViolationReturnValueError(ContractViolationError):
    """Ошибка нарушения контракта возвращаемого значения."""


class ContractViolationInvariantError(ContractViolationError):
    """Ошибка нарушения типа значения."""


class ContractViolationHasNoPermissionError(ContractViolationError):
    """Ошибка нарушения прав доступа."""
