from typing import Any

from core.http_codes import HTTP_422_UNPROCESSABLE_ENTITY
from domain.exceptions.base import DomainError
from core.error_codes import ErrorCodes


class DomainValidationError(DomainError):
    """ Базовое исключение для ошибок валидации. """

    code = ErrorCodes.VALIDATION_ERROR
    message = ErrorCodes.VALIDATION_ERROR
    http_status = HTTP_422_UNPROCESSABLE_ENTITY


class DomainFieldValidationErrorError(DomainValidationError):
    """Класс исключения для ошибок валидации типа."""

    detail_pattern = (
        "Ошибка валидации поля: {!r} у {!r}. "
        "Значение={!r}. "
        "Описание ошибки: {!r}. "
    )

    def __init__(
        self,
        *,
        subject: str,
        field: str,
        message: str,
        value: Any = None,
        error_code: str | None = None,
    ):
        super().__init__(
            message=message,
            detail=self.detail_pattern.format(field, subject, value, message),
            code=error_code,
        )


# class ContractViolationInvariantError(DomainValidationError):
#     """ Нарушение контракта инварианта. """
#
#
# class ContractViolationValueTypeError(DomainValidationError):
#     """Нарушение контракта типа значения."""
#
#
# class ContractViolationBusinessRulesError(DomainValidationError):
#     """Нарушение контракта бизнес-правил."""
#
#
# class ContractViolationHasNoPermissionError(DomainValidationError):
#     """Ошибка нарушения прав доступа."""
