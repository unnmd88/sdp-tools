from core.error_data import ErrorData
from core.exceptions import BaseAppError


class DomainError(BaseAppError):
    """
    Базовое исключение домена.
    Все доменные исключения должны наследоваться от него.
    """

    DEFAULT_CODE = ErrorData.DOMAIN_ERROR.code
    DEFAULT_MESSAGE = ErrorData.DOMAIN_ERROR.message


class DomainContractViolationError(DomainError):

    DEFAULT_CODE = ErrorData.DOMAIN_CONTRACT_VIOLATION.code
    DEFAULT_MESSAGE = ErrorData.DOMAIN_CONTRACT_VIOLATION.message


class DomainValidationError(DomainContractViolationError):
    """Базовое исключение для ошибок валидации."""

    DEFAULT_CODE = ErrorData.DOMAIN_VALIDATION.code
    DEFAULT_MESSAGE = ErrorData.DOMAIN_VALIDATION.message


class DomainBusinessRuleError(DomainContractViolationError):
    """Нарушение бизнес-правил."""

    DEFAULT_CODE = ErrorData.BUSINESS_RULE_VIOLATION.code
    DEFAULT_MESSAGE = ErrorData.BUSINESS_RULE_VIOLATION.message


class DomainInvariantError(DomainContractViolationError):
    """Нарушение инварианта."""

    DEFAULT_CODE = ErrorData.DOMAIN_INVARIANT_VIOLATION.code
    DEFAULT_MESSAGE = ErrorData.DOMAIN_INVARIANT_VIOLATION.message


class DomainEntityNotFoundError(DomainContractViolationError):
    """ Сущность не найдена. """

    DEFAULT_CODE = ErrorData.ENTITY_NOT_FOUND.code
    DEFAULT_MESSAGE = ErrorData.ENTITY_NOT_FOUND.message