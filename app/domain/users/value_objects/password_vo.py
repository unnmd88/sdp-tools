from dataclasses import dataclass, field

from core.error_data import ErrorData
from domain.enums.attrs_names import PrivateAttrNamesEnum
from domain.enums.validation_err_messages import ErrorMessages
from domain.enums.violations import Violations
from domain._exceptions.base import DomainError
from domain._exceptions.contract_violation_exc import (
    DomainValidationError,
    DomainBusinessRuleError,
)


@dataclass(frozen=True, slots=True, kw_only=True, repr=False)
class PasswordVO:
    password: str | bytes
    subject: str = str(PrivateAttrNamesEnum.password)

    def __post_init__(self):
        if self.password and isinstance(self.password, str | bytes):
            return
        rule = None
        if not isinstance(self.password, str | bytes):
            violation = Violations.invalid_type
            message = ErrorMessages.expected_string_or_bytes.format(
                str(PrivateAttrNamesEnum.password)
            )
        elif len(self.password) == 0:
            violation = Violations.cannot_be_empty
            rule = ErrorMessages.password_can_not_be_empty
            message = rule
        else:
            raise DomainError
        exc = DomainValidationError if not rule else DomainBusinessRuleError
        contract_code = (
            ErrorData.DOMAIN_VALIDATION.code
            if not rule
            else ErrorData.BUSINESS_RULE_VIOLATION.code
        )
        raise exc(
            subject=self.subject,
            field_name=str(PrivateAttrNamesEnum.password),
            handler=repr(self.__class__.__name__),
            contract_code=contract_code,
            violation=violation,
            rule=rule,
            value=self.password,
            message=message,
        )

    def __repr__(self):
        return f"{self.__class__.__name__}(password=******)"


if __name__ == "__main__":
    p = PasswordVO("1231")
    print(p)
