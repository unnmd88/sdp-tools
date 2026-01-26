from domain._exceptions.base import DomainError


class DomainContractViolationError(DomainError):

    DEFAULT_CODE = "DOMAIN_CONTRACT_VIOLATION"
    DEFAULT_MESSAGE = "Нарушение контракта."


class DomainValidationError(DomainContractViolationError):
    """Базовое исключение для ошибок валидации."""

    DEFAULT_CODE = "DOMAIN_VALIDATION_ERROR"
    DEFAULT_MESSAGE = "Ошибка валидации."


class DomainBusinessRuleError(DomainContractViolationError):
    """Нарушение бизнес-правил."""

    DEFAULT_CODE = "DOMAIN_BUSINESS_RULE_VIOLATION"
    DEFAULT_MESSAGE = "Нарушение бизнес-правил."


class DomainInvariantError(DomainContractViolationError):
    """Нарушение инварианта."""

    DEFAULT_CODE = "DOMAIN_INVARIANT_VIOLATION"
    DEFAULT_MESSAGE = "Нарушение инварианта."
