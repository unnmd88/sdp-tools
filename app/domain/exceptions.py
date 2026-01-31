from core.error_codes import ErrorCodes
from core.exceptions import BaseAppError


class DomainError(BaseAppError):
    """
    Базовое исключение домена.
    Все доменные исключения должны наследоваться от него.
    """

    DEFAULT_CODE = ErrorCodes.DOMAIN_ERROR.code
    DEFAULT_MESSAGE = ErrorCodes.DOMAIN_ERROR.message


class DomainContractViolationError(DomainError):
    DEFAULT_CODE = ErrorCodes.DOMAIN_CONTRACT_VIOLATION.code
    DEFAULT_MESSAGE = ErrorCodes.DOMAIN_CONTRACT_VIOLATION.message


class DomainValidationError(DomainContractViolationError):
    """Базовое исключение для ошибок валидации."""

    DEFAULT_CODE = ErrorCodes.DOMAIN_VALIDATION.code
    DEFAULT_MESSAGE = ErrorCodes.DOMAIN_VALIDATION.message


class DomainBusinessRuleError(DomainContractViolationError):
    """Нарушение бизнес-правил."""

    DEFAULT_CODE = ErrorCodes.BUSINESS_RULE_VIOLATION.code
    DEFAULT_MESSAGE = ErrorCodes.BUSINESS_RULE_VIOLATION.message


class DomainInvariantError(DomainContractViolationError):
    """Нарушение инварианта."""

    DEFAULT_CODE = ErrorCodes.DOMAIN_INVARIANT_VIOLATION.code
    DEFAULT_MESSAGE = ErrorCodes.DOMAIN_INVARIANT_VIOLATION.message


class DomainEntityNotFoundError(DomainError):
    """Сущность не найдена."""

    DEFAULT_CODE = ErrorCodes.ENTITY_NOT_FOUND.code
    DEFAULT_MESSAGE = ErrorCodes.ENTITY_NOT_FOUND.message


class DomainEntityAlreadyExistsError(DomainError):
    DEFAULT_CODE = ErrorCodes.ENTITY_ALREADY_EXISTS.code
    DEFAULT_MESSAGE = ErrorCodes.ENTITY_ALREADY_EXISTS.message
