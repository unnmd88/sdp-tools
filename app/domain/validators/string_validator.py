from dataclasses import dataclass

from core.error_codes import ErrorCodes
from domain.enums.validation_err_messages import ErrorMessages
from domain.enums.violations import Violations
from domain.exceptions import DomainValidationError, DomainBusinessRuleError
from domain.value_objects.contract_violation_context_vo import ContractViolationContextVO


@dataclass(frozen=True, kw_only=True, slots=True)
class StringValidator:
    min_length: int
    max_length: int

    def __post_init__(self):
        if not isinstance(self.min_length, int):
            raise TypeError("min_length должен быть целым числом")
        if not isinstance(self.max_length, int):
            raise TypeError("max_length должен быть целым числом")

    def __call__(self, value: str) -> str:
        if isinstance(value, str) and (len(value) >= self.min_length) and (len(value) <= self.max_length):
            return value

        if not isinstance(value, str):
            message = ErrorMessages.must_be_string
            contract_code = ErrorCodes.VALIDATION_ERROR.code
            violation = Violations.invalid_type
            exc = DomainValidationError
        else:
            if len(value) < self.min_length:
                message = ErrorMessages.string_too_short.format(self.min_length, len(value))
            else:
                message = ErrorMessages.string_too_long.format(self.max_length, len(value))
            contract_code = ErrorCodes.BUSINESS_RULE_VIOLATION.code
            violation = Violations.invalid_length
            exc = DomainBusinessRuleError
        context = ContractViolationContextVO(
            handler=f"{self.__class__.__name__!r}:{self.__call__.__name__!r}",
            contract_code=contract_code,
            violation=violation,
            value=value,
            expected_type=str,
            message=message,
        )
        raise exc(
            context=context,
            private_message=message,
            public_message=message
        )



if __name__ == '__main__':
    iv = StringValidator(min_length=1, max_length=32)
    print(iv(""))