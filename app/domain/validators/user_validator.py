from core.error_data import ErrorData
from domain.enums.validation_err_messages import ErrorMessages
from domain.enums.public_attrs import PublicAttrsEnum
from domain.enums.violations import Violations
from domain.exceptions.base import DomainError
from domain.exceptions.contract_violation_exc import DomainValidationError, DomainBusinessRuleError
from domain.users.business_rules import (
    MIN_LEN_FIRSTNAME,
    MAX_LEN_FIRSTNAME,
    MIN_LEN_USERNAME,
    MAX_LEN_USERNAME,
    MIN_LEN_LASTNAME,
    MAX_LEN_LASTNAME,
)


class UserEntityValidator:

    subject: str = "UserEntity"

    @classmethod
    def username(cls, value: str) -> bool:
        if isinstance(value, str) and not value.isnumeric() and (MIN_LEN_USERNAME <= len(value) <= MAX_LEN_USERNAME) and not value[0].isdigit():
            return True
        field_name = str(PublicAttrsEnum.username)
        is_business_rule = False
        rule = None
        if not isinstance(value, str):
            violation = Violations.invalid_type
            message = ErrorMessages.expected_type_string
        elif value.isnumeric():
            violation = Violations.invalid_type
            rule = ErrorMessages.cant_be_numeric.format(field_name, value)
            message = rule
            is_business_rule = True
        elif value[0].isdigit():
            is_business_rule = True
            violation = Violations.string_cant_start_with_numeric
            rule = ErrorMessages.cant_start_with_numeric.format(field_name, value)
            message = rule
        elif not (MIN_LEN_USERNAME <= len(value) <= MAX_LEN_USERNAME):
            is_business_rule = True
            violation = Violations.value_length
            rule = ErrorMessages.value_str_length_range.format(
                field_name, len(value), MIN_LEN_USERNAME, MAX_LEN_USERNAME
            )
            message = rule
        else:
            raise DomainError
        exc = DomainValidationError if not is_business_rule else DomainBusinessRuleError
        raise exc(
            subject=cls.subject,
            field_name=field_name,
            handler=repr(cls.username.__name__),
            contract_name=ErrorData.BUSINESS_RULE_VIOLATION.code,
            violation=violation,
            rule=rule,
            value=value,
            message=message,
        )

    @classmethod
    def first_name_or_lastname(
        cls,
        value: str,
        field_name,
        min_len: int,
        max_len: int,
        handler: str,
    ) -> bool:
        if isinstance(value, str) and value.isalpha() and (min_len <= len(value) <= max_len):
            return True
        if not isinstance(value, str):
            violation = Violations.invalid_type
            message = ErrorMessages.expected_type_string
        elif not value.isalpha():
            violation = Violations.string_cant_be_numeric
            message = ErrorMessages.must_be_isalpha.format(value)
        elif min_len <= len(value) <= max_len:
            violation = Violations.value_length
            message = ErrorMessages.value_str_length_range.format(
                field_name, len(value), min_len, max_len,
                )
        else:
            raise DomainError
        raise DomainValidationError(
            subject=cls.subject,
            field_name=field_name,
            handler=handler,
            contract_name=ErrorData.DOMAIN_VALIDATION.code,
            violation=violation,
            value=value,
            message=message,
        )

    @classmethod
    def firstname(cls, value: str) -> bool:
        return cls.first_name_or_lastname(
            value=value,
            field_name=str(PublicAttrsEnum.firstname),
            min_len=MIN_LEN_FIRSTNAME,
            max_len=MAX_LEN_FIRSTNAME,
            handler=cls.firstname.__name__,
        )

    @classmethod
    def lastname(cls, value: str) -> bool:
        return cls.first_name_or_lastname(
            value=value,
            field_name=str(PublicAttrsEnum.lastname),
            min_len=MIN_LEN_LASTNAME,
            max_len=MAX_LEN_LASTNAME,
            handler=cls.firstname.__name__,
        )

    @classmethod
    def repair_name(cls, value: str) -> str:
        return value.strip().capitalize() if isinstance(value, str) else value

