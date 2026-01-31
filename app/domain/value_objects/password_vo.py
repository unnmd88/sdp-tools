from dataclasses import dataclass, field

from core.error_codes import ErrorCodes
from domain.enums.attrs_names import PrivateAttrNamesEnum
from domain.enums.validation_err_messages import ErrorMessages
from domain.enums.violations import Violations
from domain.exceptions import (
    DomainError,
    DomainBusinessRuleError,
    DomainValidationError,
)
from domain.value_objects.contract_violation_context_vo import (
    ContractViolationContextVO,
)


@dataclass(frozen=True, slots=True, kw_only=True, repr=False)
class PasswordVO:
    password: str | bytes
    subject: str

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
            ErrorCodes.DOMAIN_VALIDATION.code
            if not rule
            else ErrorCodes.BUSINESS_RULE_VIOLATION.code
        )
        ctx = ContractViolationContextVO(
            subject=self.subject,
            field_name=str(PrivateAttrNamesEnum.password),
            handler=repr(self.__post_init__.__name__),
            contract_code=contract_code,
            violation=violation,
            rule=rule,
            value=self.password,
            message=message,
        )
        raise exc(context=ctx)

    def __repr__(self):
        return f"{self.__class__.__name__}(password=******)"


if __name__ == "__main__":
    p = PasswordVO("1231")
    print(p)
