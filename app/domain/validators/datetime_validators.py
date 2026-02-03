from dataclasses import dataclass
from datetime import datetime

from core.error_codes import ErrorCodes
from domain.enums.attrs_names import PublicAttrNamesEnum
from domain.enums.validation_err_messages import ErrorMessages
from domain.enums.violations import Violations
from domain.exceptions import DomainValidationError


# from domain._exceptions.contract_violation_exc import DomainValidationError
#


@dataclass(frozen=True, slots=True, kw_only=True)
class DatetimeValidators:
    field_name: str

    def __call__(self, value: datetime) -> datetime:
        if isinstance(value, datetime):
            return value
        raise DomainValidationError(
            field_name=self.field_name,
            handler=repr(self.__class__.__name__),
            contract_code=ErrorCodes.DOMAIN_VALIDATION.code,
            violation=Violations.invalid_type,
            value=value,
            private_message=ErrorMessages.must_be_valid_datetime.format(self.field_name, value),
            public_message=ErrorMessages.must_be_valid_datetime.format(self.field_name, value),
        )
