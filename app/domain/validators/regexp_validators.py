import re

from core.error_codes import ErrorCodes
from domain.kernel.enums.attrs_names import PublicAttrNamesEnum
from domain.kernel.enums.validation_err_messages import ErrorMessages

from domain.kernel.enums.violations import Violations

from domain.kernel.business_rules import (
    EMAIL_PATTERN,
    PHONE_NUMBER_PATTERN,
    TELEGRAM_PATTERN,
)
from domain.exceptions import DomainValidationError
from domain.value_objects.contract_violation_context_vo import (
    ContractViolationContextVO,
)


class RegexpValidator:
    regexp_contract_code: str = ErrorCodes.DOMAIN_VALIDATION.code
    regexp_violation: Violations = Violations.does_not_match_regexp
    pattern = None
    field_name = None

    def __init__(
        self,
        *,
        pattern: re.Pattern | str = None,
        field_name: str = None,
        regexp_contract_code: str = None,
        regexp_violation: Violations = None,
    ):
        if pattern is not None:
            self._pattern = (
                pattern if isinstance(pattern, re.Pattern) else re.compile(pattern)
            )
        else:
            self._pattern = self.pattern
        self._regexp_contract_code = regexp_contract_code or self.regexp_contract_code
        self._regexp_violation = regexp_violation or self.regexp_violation
        self._field_name = field_name or self.field_name or "unknown"

    def __call__(self, value) -> bool:
        if (
            isinstance(value, str)
            and re.match(self._pattern.pattern, value) is not None
        ):
            return True
        if not isinstance(value, str):
            violation = str(Violations.invalid_type)
            message = ErrorMessages.expected_type_string.format(self._field_name, value)
        else:
            violation = self._regexp_violation
            message = ErrorMessages.invalid_format.format(self._field_name, value)
        ctx = ContractViolationContextVO(
            field_name=self._field_name,
            handler=self.__class__.__name__,
            contract_code=self._regexp_contract_code,
            violation=violation,
            value=value,
            message=message,
        )
        raise DomainValidationError(
            context=ctx,
            private_message=f"Входные данные не соответствуют шаблону регулярного выражения поля {self.field_name!r}.",
            public_message=f"Некорректный формат данных для поля {self.field_name!r}.",
        )

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"contract_code={self._regexp_contract_code} "
            f"violation={self._regexp_violation} "
            f"field_name={self.field_name!r} "
            f")"
        )


class EmailRegexpValidator(RegexpValidator):
    pattern = EMAIL_PATTERN
    field_name = str(PublicAttrNamesEnum.email)


class PhoneNumberRegexpValidator(RegexpValidator):
    pattern = PHONE_NUMBER_PATTERN
    field_name = str(PublicAttrNamesEnum.phone_number)


class TelegramRegexpValidator(RegexpValidator):
    pattern = TELEGRAM_PATTERN
    field_name = str(PublicAttrNamesEnum.telegram)


if __name__ == "__main__":
    email = EmailRegexpValidator()
    phone_number = PhoneNumberRegexpValidator()
    telegram = TelegramRegexpValidator()
    try:
        email("dasdadail@ruba.com")
    except DomainValidationError as e:
        print(e)
        print(e.to_dict())
        raise e
    phone_number = PhoneNumberRegexpValidator()
    print(phone_number)
    try:
        phone_number("9999799999")
    except DomainValidationError as e:
        print(e)
        print(e.to_dict())
        raise e
