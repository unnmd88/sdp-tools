from dataclasses import dataclass, field
from enum import Enum
from types import UnionType
from typing import Any

from core.error_data import ErrorData
from domain.enums.validation_err_messages import ErrorMessages
from domain.enums.public_attrs import PublicAttrsEnum
from domain.enums.violations import Violations
from domain.exceptions.base import DomainError
from domain.exceptions.contract_violation_exc import (
    DomainValidationError,
    DomainBusinessRuleError,
)
from domain.users.business_rules import (
    EMAIL_PATTERN,
    PHONE_NUMBER_PATTERN,
    MIN_LEN_FIRSTNAME,
    MAX_LEN_FIRSTNAME,
    MIN_LEN_USERNAME,
    MAX_LEN_USERNAME,
)
from domain.users.entities.user import UserEntity
from domain.utils import validate_string_by_pattern


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
