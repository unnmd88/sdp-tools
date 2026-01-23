from enum import StrEnum
from types import UnionType
from typing import Any

from core.error_data import ErrorData
from domain.exceptions.base import DomainError


class DomainContractViolationError(DomainError):
    def __init__(
        self,
        *,
        subject: Any = None,
        handler: str | None = None,
        field_name: str,
        contract_code: str,
        violation: str | StrEnum,
        value: Any = None,
        expected_type: type | UnionType | tuple[type] = None,
        rule: str | None = None,
        error_code: str | None = None,
        context: dict[str, Any] | None = None,
        message: str = "",
    ):
        super().__init__(
            message=message or self.message,
            code=error_code,
            subject=subject,
            context=context,
        )
        self.handler = handler
        self.violation = violation
        self.field_name = field_name
        self.value = value
        self.expected_type = expected_type
        self.contract_code = contract_code
        self.rule = rule
        self.context |= {
            "subject": self.subject,
            "field_name": self.field_name,
            "value": self.value,
            "handler": self.handler,
            "contract_code": self.contract_code,
            "violation": self.violation,
            "expected_type": repr(self.expected_type) if self.expected_type else None,
            "rule": self.rule,
            "current_type": repr(type(value)),
            "message": self.message,
        }


class DomainValidationError(DomainContractViolationError):
    """Базовое исключение для ошибок валидации."""

    code = ErrorData.VALIDATION_ERROR.code
    message = ErrorData.VALIDATION_ERROR.message
    http_status = ErrorData.VALIDATION_ERROR.http_status_code


class DomainBusinessRuleError(DomainContractViolationError):
    """Нарушение бизнес-правил."""

    code = ErrorData.BUSINESS_RULE_VIOLATION.code
    message = ErrorData.BUSINESS_RULE_VIOLATION.message
    http_status = ErrorData.BUSINESS_RULE_VIOLATION.http_status_code


class DomainInvariantViolationBusinessRuleError(DomainBusinessRuleError):
    """Нарушение инварианта."""

    code = ErrorData.DOMAIN_INVARIANT_VIOLATION.code
    message = ErrorData.DOMAIN_INVARIANT_VIOLATION.message
    http_status = ErrorData.DOMAIN_INVARIANT_VIOLATION.http_status_code
