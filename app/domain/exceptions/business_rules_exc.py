from core.http_codes import HTTP_409_CONFLICT
from core.error_codes import ErrorCodes
from domain.exceptions.base import DomainError


class DomainBusinessRuleError(DomainError):
    """Нарушение бизнес-правил."""

    code = ErrorCodes.BUSINESS_RULE_ERROR
    message = ErrorCodes.BUSINESS_RULE_VIOLATION
    http_status = HTTP_409_CONFLICT


class DomainInvariantViolationBusinessRuleError(DomainBusinessRuleError):
    """Нарушение инварианта."""

    code = ErrorCodes.INVARIANT_VIOLATION

