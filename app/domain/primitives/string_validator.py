import re
from typing import Self

from core.error_codes import ErrorCodes
from domain.enums.validation_err_messages import ErrorMessages
from domain.enums.violations import Violations
from domain.exceptions import DomainValidationError, DomainBusinessRuleError, DomainContractViolationError
from domain.value_objects.contract_violation_context_vo import ContractViolationContextVO


class StringValidator:

    __slots__ = ("_value", "_field_name")

    def __init__(
        self,
        *,
        value: str,
        field_name: str,
    ):
        self._value = value
        self._field_name = field_name

    @classmethod
    def validate_of(cls, value: str, field_name: str) -> Self:
        return cls(value=value, field_name=field_name)

    def ensure_not_empty(self, exception: type[DomainValidationError] = DomainValidationError,) -> Self:
        """Проверить, что не пустая строка."""
        if not self._value:
            message = ErrorMessages.string_for_field_cant_be_empty.format(self._value)
            contract_code = ErrorCodes.DOMAIN_VALIDATION.code
            violation = Violations.cannot_be_empty
            context = ContractViolationContextVO(
                handler=f"{self.__class__.__name__!r}:{self.ensure_not_empty.__name__!r}",
                contract_code=contract_code,
                violation=violation,
                value=self._value,
                expected_type=str,
                message=message,
            )
            raise exception(private_message=message, public_message=message, context=context)
        return self

    def ensure_min_length(
        self,
        length: int,
        exception: type[DomainValidationError] = DomainValidationError,
    ) -> Self:
        """Минимальная длина."""
        message = ErrorMessages.string_too_short.format(length, len(self._value))
        if len(self._value) < length:
            contract_code = ErrorCodes.DOMAIN_VALIDATION.code
            violation = Violations.invalid_length
            context = ContractViolationContextVO(
            handler=f"{self.__class__.__name__!r}:{self.ensure_min_length.__name__!r}",
            contract_code=contract_code,
            violation=violation,
            value=self._value,
            expected_type=str,
            message=message,
        )
            raise exception(private_message=message, public_message=message, context=context)
        return self

    def ensure_max_length(
        self,
        length: int,
        exception: type[DomainValidationError] = DomainValidationError
    ) -> Self:
        """Минимальная длина."""
        if len(self._value) < length:
            message = ErrorMessages.string_too_long.format(length, len(self._value))
            contract_code = ErrorCodes.DOMAIN_VALIDATION.code
            violation = Violations.invalid_length
            context = ContractViolationContextVO(
                handler=f"{self.__class__.__name__!r}:{self.ensure_min_length.__name__!r}",
                contract_code=contract_code,
                violation=violation,
                value=self._value,
                expected_type=str,
                message=self._exception.message,
            )
            raise exception(private_message=message, public_message=message, context=context)
        return self

    def ensure_matches(
        self,
        *,
        pattern: str | re.Pattern,
        public_message: str = ErrorMessages.invalid_field_format,
        exception: type[DomainValidationError] = DomainValidationError,
    ) -> Self:
        """Соответствует regex шаблону."""

        if not re.match(pattern, self._value):
            private_message = ErrorMessages.regex_pattern_mismatch.format(self._value, pattern)
            if public_message == ErrorMessages.invalid_field_format:
                public_message = private_message.format(self._value)
            else:
                public_message = public_message
            context = ContractViolationContextVO(
                handler=f"{self.__class__.__name__!r}:{self.ensure_matches.__name__!r}",
                contract_code=ErrorCodes.DOMAIN_VALIDATION.code,
                violation=Violations.pattern_mismatch,
                value=self._value,
                field_name=self._field_name,
                expected_pattern=pattern,
                message=private_message,
            )
            raise exception(private_message=private_message, public_message=public_message,context=context)
        return self

    def get(self) -> str:
        return self._value


if __name__ == '__main__':
    e = ValueError("test", "test1")
    print(e.args)