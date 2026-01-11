from enum import Enum
from typing import Any

from core.reg_exps import EMAIL_PATTERN, PHONE_NUMBER_PATTERN
from core.users.constants import MIN_ID, MAX_ID
from core.utils import validate_string_by_pattern


def id_validator(value: int) -> bool:
    return MIN_ID < value < MAX_ID


class EnumValidator:
    def __init__(self, enum_cls: type[Enum]):
        self._enum_cls = enum_cls

    def __call__(self, value: Any) -> bool:
        try:
            self._enum_cls(value)
        except ValueError:
            return False
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
