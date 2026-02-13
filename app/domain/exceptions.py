from typing import Any, Self

from core.enums import ContextKey
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

    def with_field(self, field: str) -> Self:
        self._with_context_by_dict({ContextKey.FIELD: field})
        return self

    def with_rule_if_has_not(self, rule: str) -> Self:
        self._with_context_by_dict({ContextKey.RULE: rule})
        return self

    def with_validator_if_has_not(self, validator: str) -> Self:
        self._with_context_by_dict({ContextKey.VALIDATOR: validator})
        return self

    def with_expected(self, expected: Any) -> Self:
        """Добавляет ожидаемое значение."""
        self._with_context_by_dict({ContextKey.EXPECTED: str(expected)})
        return self


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


if __name__ == '__main__':
    try:
        e =  (
            DomainContractViolationError(public_message='test', private_message='public message test')
            .with_entity_context(entity='test', entity_id=1)
            .with_validator_if_has_not('test')
        )
        print(e)
        print(e.to_dict())
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++")
        raise e
    except DomainContractViolationError as e:
        e.with_field("test_field")
        print(e)
        print(e.to_dict())
        raise e
