import re
from collections.abc import Container
from dataclasses import dataclass, field
from typing import Any

from core.error_data import ErrorData
from domain.enums.attrs_names import PublicAttrNamesEnum
from domain.enums.validation_err_messages import ErrorMessages
from domain.enums.violations import Violations
from domain._exceptions.contract_violation_exc import DomainValidationError
from domain.users.business_rules import EMAIL_PATTERN


@dataclass(frozen=True, kw_only=True, slots=True)
class BooleanValidator:
    field_name: str
    allowed_like_bool: Container = ()

    def __call__(self, value: Any) -> bool:
        if isinstance(value, bool) or (value in self.allowed_like_bool):
            return bool(value)
        msg = ErrorMessages.expected_bool.format(self.field_name)
        raise DomainValidationError(
            field_name=self.field_name,
            handler=self.__class__.__name__,
            contract_code=ErrorData.DOMAIN_VALIDATION.code,
            violation=Violations.invalid_type,
            value=msg,
            message=msg,
        )
