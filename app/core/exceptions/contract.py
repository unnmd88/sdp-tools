from core.exceptions.base import DomainValidationError


class ContractViolationError(DomainValidationError):
    """Базовый класс ошибки валидации контракта."""


class ContractViolationInvariantError(ContractViolationError):
    """Ошибка инварианта контракта."""
