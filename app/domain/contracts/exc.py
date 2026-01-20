from typing import Any


class ContractViolationError(Exception):
    """Базовый класс для исключений, возникающих при нарушении контракта."""

    def __init__(
        self,
        *,
        field_name: str,
        handler: Any = None,
        # contract: str = None,
        # violation: str = None,
        value: Any = None,
        context: Any = None,
        message: str = "",
    ):
        self.handler = handler
        # self.contract = contract
        # self.violation = violation
        self.field_name = field_name
        self.value = value
        self.context = context
        self.message = message
        # self.expected_type = expected_type
        # self.message = (
        #     f"contract={self.contract!r}. "
        #     f"violation={self.violation!r}. "
        #     f"value={self.value!r} "
        #     f"field={self.field_name!r} "
        #     f"context={self.context!r}. "
        #     f"expected_type={expected_type or ''!r}."
        # )
        super().__init__(self.message)


class ContractViolationPreProcessingError(ContractViolationError):
    """Класс исключений, возникающих при нарушении контракта предобработки."""


class ContractViolationNotNoneError(ContractViolationError):
    """Класс исключений, возникающих при нарушении контракта 'not None'."""


class ContractViolationFieldError(ContractViolationError):
    """Класс исключений, возникающих при нарушении контракта поля."""


class ContractViolationInvariantError(ContractViolationError):
    """Ошибка нарушения типа значения."""
