from dataclasses import dataclass, field
from enum import Enum
from types import UnionType
from typing import Any

from core.error_data import ErrorData
from domain.enums.business_rules import BusinessRulePatterns
from domain.enums.public_attrs import PublicAttrsEnum
from domain.enums.violations import Violations
from domain.users.business_rules import (
    MIN_ID,
    MAX_ID,
    EMAIL_PATTERN,
    PHONE_NUMBER_PATTERN, MIN_LEN_FIRSTNAME, MAX_LEN_FIRSTNAME, MIN_LEN_USERNAME, MAX_LEN_USERNAME,
)
from domain.users.rules_messages import DomainRulesViolationsMessages
from domain.utils import validate_string_by_pattern

@dataclass(kw_only=True, frozen=True, slots=True)
class ValidatorException(Exception):
    field_name: str
    handler: str
    contract_name: str
    violation: str
    value: Any
    expected_type: type = None
    rule: str = None
    message: str = ""
    context: dict[str, Any] = field(default_factory=dict)


def username_validator(value: str) -> bool:
    print("username_validator")
    if not isinstance(value, str):
        raise ValidatorException(
            field_name=str(PublicAttrsEnum.username),
            handler=repr(username_validator.__name__),
            contract_name=ErrorData.DOMAIN_VALIDATION.code,
            violation=Violations.invalid_type,
            message="Значение должно быть строкой",
            value=value,
            expected_type=str,
        )
    if not MIN_LEN_USERNAME <= len(value) <= MAX_LEN_USERNAME:
        if len(value) <= MIN_LEN_FIRSTNAME:
            pass #TODO детализировать, что меньше минимума
        else:
            pass # TODO детализировать, что больше максимума
        raise ValidatorException(
            field_name=str(PublicAttrsEnum.username),
            handler=repr(username_validator.__name__),
            contract_name=ErrorData.BUSINESS_RULE_VIOLATION.code,
            violation=Violations.value_length,
            rule=BusinessRulePatterns.username_length_range,
            value=value,
            message=BusinessRulePatterns.username_length_range,
        )
    print("username_validator  True")
    return True


def email_validator(value: str) -> bool:
    return validate_string_by_pattern(value, EMAIL_PATTERN)


def password_validator(value: bytes) -> bool:
    """
    Проверяет валидность password.
    :param value: Строка password.
    :return: True or False.
    """
    return len(value) > 2


def phone_number_validator(value: str) -> bool:
    """
    Проверяет валидность phone_number.
    :param value: Строка phone_number.
    :return: True or False.
    """
    return validate_string_by_pattern(value, PHONE_NUMBER_PATTERN)


def description_validator(value: str) -> bool:
    """
    Проверяет валидность description.
    :param value: Строка description.
    :return: True or False.
    """
    return len(value) < 255
