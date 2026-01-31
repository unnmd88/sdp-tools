from collections.abc import Container
from dataclasses import dataclass
from typing import Any

from core.error_codes import ErrorCodes
from domain.enums.validation_err_messages import ErrorMessages
from domain.enums.violations import Violations
from domain.exceptions import DomainValidationError
from domain.value_objects.contract_violation_context_vo import (
    ContractViolationContextVO,
)


@dataclass(frozen=True, kw_only=True, slots=True)
class BooleanValidator:
    field_name: str
    allowed_like_bool: Container = ()

    def __call__(self, value: Any) -> bool:
        if isinstance(value, bool) or (value in self.allowed_like_bool):
            return bool(value)
        msg = ErrorMessages.expected_bool.format(self.field_name)
        ctx = ContractViolationContextVO(
            field_name=self.field_name,
            handler=f"{self.__class__.__name__}:{self.__call__.__name__}",
            contract_code=ErrorCodes.DOMAIN_VALIDATION.code,
            violation=Violations.invalid_type,
            value=msg,
            message=msg,
        )
        raise DomainValidationError(context=ctx)
