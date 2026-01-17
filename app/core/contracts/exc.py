from typing import Any


class ContractViolationError(Exception):
    """Базовый класс для исключений, возникающих при нарушении контракта."""

    def __init__(
        self,
        *,
        contract: str = "",
        violation: str = "",
        field_name: str = "",
        value: Any = None,
        detail: str = "",
    ):
        self.contract = contract
        self.violation = violation
        self.value = value
        self.field_name = field_name
        self.detail = detail
        self.message = (
            f"Контракт={self.contract!r}. "
            f"Нарушение={self.violation!r}. "
            f"Значение={self.value!r} "
            f"Поле={self.field_name!r} "
            f"detail={self.detail!r}."
        )
        super().__init__(self.message)


class ContractViolationPreProcessingError(ContractViolationError):
    """Класс исключений, возникающих при нарушении контракта предобработки."""


class ContractViolationFieldError(ContractViolationError):
    """Класс исключений, возникающих при нарушении контракта поля."""


class ContractViolationBusinessRulesError(ContractViolationError):
    """Ошибка нарушения контракта бизнес-правил."""


class ContractViolationReturnValueError(ContractViolationError):
    """Ошибка нарушения контракта возвращаемого значения."""


class ContractViolationInvariantError(ContractViolationError):
    """Ошибка нарушения типа значения."""


class ContractViolationHasNoPermissionError(ContractViolationError):
    """Ошибка нарушения прав доступа."""
