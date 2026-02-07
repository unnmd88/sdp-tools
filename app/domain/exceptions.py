from core.error_codes import ErrorCodes
from core.exceptions import BaseAppError


class DomainError(BaseAppError):
    """
    Базовое исключение домена.
    Все доменные исключения должны наследоваться от него.
    """

    DEFAULT_CODE = ErrorCodes.DOMAIN_ERROR.code
    DEFAULT_PRIVATE_MESSAGE = ErrorCodes.DOMAIN_ERROR.private_message
    DEFAULT_PUBLIC_MESSAGE = ErrorCodes.DOMAIN_ERROR.public_message


class DomainContractViolationError(DomainError):
    DEFAULT_CODE = ErrorCodes.DOMAIN_CONTRACT_VIOLATION.code
    DEFAULT_PRIVATE_MESSAGE = ErrorCodes.DOMAIN_CONTRACT_VIOLATION.private_message
    DEFAULT_PUBLIC_MESSAGE = ErrorCodes.DOMAIN_CONTRACT_VIOLATION.public_message


class DomainValidationError(DomainContractViolationError):
    """Базовое исключение для ошибок валидации."""

    DEFAULT_CODE = ErrorCodes.DOMAIN_VALIDATION.code
    DEFAULT_PRIVATE_MESSAGE = ErrorCodes.DOMAIN_VALIDATION.private_message
    DEFAULT_PUBLIC_MESSAGE = ErrorCodes.DOMAIN_VALIDATION.public_message


class DomainBusinessRuleError(DomainContractViolationError):
    """Нарушение бизнес-правил."""

    DEFAULT_CODE = ErrorCodes.BUSINESS_RULE_VIOLATION.code
    DEFAULT_PRIVATE_MESSAGE = ErrorCodes.BUSINESS_RULE_VIOLATION.private_message
    DEFAULT_PUBLIC_MESSAGE = ErrorCodes.BUSINESS_RULE_VIOLATION.public_message


class DomainInvariantError(DomainContractViolationError):
    """Нарушение инварианта."""

    DEFAULT_CODE = ErrorCodes.DOMAIN_INVARIANT_VIOLATION.code
    DEFAULT_PRIVATE_MESSAGE = ErrorCodes.DOMAIN_INVARIANT_VIOLATION.private_message
    DEFAULT_PUBLIC_MESSAGE = ErrorCodes.DOMAIN_INVARIANT_VIOLATION.public_message


class DomainEntityNotFoundError(DomainError):
    """Сущность не найдена."""

    DEFAULT_CODE = ErrorCodes.ENTITY_NOT_FOUND.code
    DEFAULT_PRIVATE_MESSAGE = ErrorCodes.ENTITY_NOT_FOUND.private_message
    DEFAULT_PUBLIC_MESSAGE = ErrorCodes.ENTITY_NOT_FOUND.public_message


class DomainEntityAlreadyExistsError(DomainError):
    DEFAULT_CODE = ErrorCodes.ENTITY_ALREADY_EXISTS.code
    DEFAULT_PRIVATE_MESSAGE = ErrorCodes.ENTITY_ALREADY_EXISTS.private_message
    DEFAULT_PUBLIC_MESSAGE = ErrorCodes.ENTITY_ALREADY_EXISTS.public_message
