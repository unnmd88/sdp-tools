from core.error_data import ErrorData
from domain.enums.validation_err_messages import ErrorMessages
from domain.enums.attrs_names import PublicAttrNamesEnum
from domain.enums.violations import Violations

from domain.business_rules import (
    MIN_LEN_FIRSTNAME,
    MAX_LEN_FIRSTNAME,
    MIN_LEN_USERNAME,
    MAX_LEN_USERNAME,
    MIN_LEN_LASTNAME,
    MAX_LEN_LASTNAME,
)
from domain.exceptions import DomainError, DomainValidationError, DomainBusinessRuleError
from domain.value_objects.contract_violation_context_vo import ContractViolationContextVO


class UserEntityValidator:
    @classmethod
    def username(cls, value: str) -> bool:
        if (
            isinstance(value, str)
            and not value.isnumeric()
            and (MIN_LEN_USERNAME <= len(value) <= MAX_LEN_USERNAME)
            and not value[0].isdigit()
        ):
            return True
        field_name = str(PublicAttrNamesEnum.username)
        rule = None
        if not isinstance(value, str):
            violation = Violations.invalid_type
            message = ErrorMessages.expected_type_string
        elif value.isnumeric():
            violation = Violations.invalid_type
            rule = ErrorMessages.cant_be_numeric.format(field_name, value)
            message = rule
        elif value[0].isdigit():
            violation = Violations.string_cant_start_with_numeric
            rule = ErrorMessages.cant_start_with_numeric.format(field_name, value)
            message = rule
        elif not (MIN_LEN_USERNAME <= len(value) <= MAX_LEN_USERNAME):
            violation = Violations.value_length
            rule = ErrorMessages.value_str_length_range.format(
                field_name, len(value), MIN_LEN_USERNAME, MAX_LEN_USERNAME
            )
            message = rule
        else:
            raise DomainError
        exc = DomainValidationError if not rule else DomainBusinessRuleError
        contract_code = (
            ErrorData.DOMAIN_VALIDATION.code
            if not rule
            else ErrorData.BUSINESS_RULE_VIOLATION.code
        )
        ctx = ContractViolationContextVO(
            field_name=field_name,
            handler=f"{cls.__name__}:{cls.username.__name__}",
            contract_code=contract_code,
            violation=violation,
            rule=rule,
            value=value,
            message=message,
        )
        raise exc(context=ctx)

    @classmethod
    def first_name_or_lastname(
        cls,
        value: str,
        field_name,
        min_len: int,
        max_len: int,
        handler: str,
    ) -> bool:
        if (
            isinstance(value, str)
            and value.isalpha()
            and (min_len <= len(value) <= max_len)
        ):
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
                field_name,
                len(value),
                min_len,
                max_len,
            )
        else:
            raise DomainError
        ctx = ContractViolationContextVO(
            field_name=field_name,
            handler=f"{cls.__name__}:{handler}",
            contract_code=ErrorData.DOMAIN_VALIDATION.code,
            violation=violation,
            value=value,
            message=message,
        )
        raise DomainValidationError(context=ctx)

    @classmethod
    def firstname(cls, value: str) -> bool:
        return cls.first_name_or_lastname(
            value=value,
            field_name=str(PublicAttrNamesEnum.firstname),
            min_len=MIN_LEN_FIRSTNAME,
            max_len=MAX_LEN_FIRSTNAME,
            handler=cls.firstname.__name__,
        )

    @classmethod
    def lastname(cls, value: str) -> bool:
        return cls.first_name_or_lastname(
            value=value,
            field_name=str(PublicAttrNamesEnum.lastname),
            min_len=MIN_LEN_LASTNAME,
            max_len=MAX_LEN_LASTNAME,
            handler=cls.firstname.__name__,
        )

    @classmethod
    def repair_firstname_or_lastname(cls, value: str) -> str:
        return value.strip().capitalize() if isinstance(value, str) else value
