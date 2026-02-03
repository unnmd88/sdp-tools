from dataclasses import dataclass
from enum import Enum, StrEnum, IntEnum
from typing import Any

from core.error_codes import ErrorCodes
from domain.enums.validation_err_messages import ErrorMessages
from domain.enums.violations import Violations
from domain.exceptions import DomainValidationError
from domain.value_objects.contract_violation_context_vo import (
    ContractViolationContextVO,
)


@dataclass(frozen=True, kw_only=True, slots=True)
class EnumValidator:
    field_name: str
    enum_class: type[Enum]

    def __call__(self, value: Any) -> Any:
        try:
            return self.enum_class(value)
        except ValueError:
            if self.enum_class == StrEnum:
                expected_type = str
            elif self.enum_class == IntEnum:
                expected_type = int
            else:
                expected_type = self.enum_class
            ctx = ContractViolationContextVO(
                field_name=self.field_name,
                handler=EnumValidator.__name__,
                contract_code=ErrorCodes.DOMAIN_VALIDATION.code,
                violation=Violations.invalid_enum_value,
                value=value,
                expected_type=expected_type,
                message=ErrorMessages.invalid_enum_value.format(
                    self.enum_class.__name__, value
                ),
            )
            raise DomainValidationError(
                context=ctx,
                public_message=ErrorMessages.must_be_member_of_enum.format(self.field_name, list(self.enum_class)),
            )
