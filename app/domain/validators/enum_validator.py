from dataclasses import dataclass
from enum import Enum
from typing import Any

from core.error_data import ErrorData
from domain.enums.validation_err_messages import ErrorMessages
from domain.enums.violations import Violations
from domain.exceptions import DomainValidationError
from domain.value_objects.contract_violation_context_vo import ContractViolationContextVO


@dataclass(frozen=True, kw_only=True, slots=True)
class EnumValidator:
    field_name: str
    enum_class: type[Enum]

    def __call__(self, value: Any) -> Any:
        try:
            return self.enum_class(value)
        except ValueError:
            ctx = ContractViolationContextVO(
                field_name=self.field_name,
                handler=EnumValidator.__name__,
                contract_code=ErrorData.DOMAIN_VALIDATION.code,
                violation=Violations.invalid_enum_value,
                value=value,
                message=ErrorMessages.invalid_enum_value.format(
                    self.enum_class.__name__, value
                ),
            )
            raise DomainValidationError(context=ctx)
