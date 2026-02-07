from dataclasses import dataclass

from core.error_codes import ErrorCodes
from domain.enums.validation_err_messages import ErrorMessages
from domain.enums.violations import Violations
from domain.exceptions import DomainValidationError, DomainBusinessRuleError
from domain.value_objects.contract_violation_context_vo import (
    ContractViolationContextVO,
)


@dataclass(frozen=True, kw_only=True, slots=True)
class IntegerValidator:
    min_value: int
    max_value: int

    def __post_init__(self):
        if not isinstance(self.min_value, int):
            raise TypeError("min_value должен быть целым числом")
        if not isinstance(self.max_value, int):
            raise TypeError("max_value должен быть целым числом")

    def __call__(self, value: int) -> int:
        if (
            isinstance(value, int)
            and (value >= self.min_value)
            and (value <= self.max_value)
        ):
            return value
        message = ErrorMessages.must_be_integer.format(self.min_value, self.max_value)
        if not isinstance(value, int):
            contract_code = ErrorCodes.VALIDATION_ERROR.code
            violation = Violations.invalid_type
            exc = DomainValidationError
        else:
            if value < self.min_value:
                message = ErrorMessages.integer_too_small.format(self.min_value, value)
            elif value > self.max_value:
                message = ErrorMessages.integer_too_large.format(self.max_value, value)
            contract_code = ErrorCodes.BUSINESS_RULE_VIOLATION.code
            violation = Violations.invalid_length
            exc = DomainBusinessRuleError
        context = ContractViolationContextVO(
            handler=f"{self.__class__.__name__!r}:{self.__call__.__name__!r}",
            contract_code=contract_code,
            violation=violation,
            value=value,
            expected_type=int,
            message=message,
        )
        raise exc(context=context, private_message=message, public_message=message)


if __name__ == "__main__":
    iv = IntegerValidator(min_value=0, max_value=100)
    print(iv(-1))
