import re
from enum import Enum
from typing import Any

from core.reg_exps import (
    EMAIL_PATTERN,
    FIRST_NAME_PATTERN,
    LAST_NAME_PATTERN,
    USERNAME_PATTERN,
    PHONE_NUMBER_PATTERN,
    PASSWORD_PATTERN,
)
from core.users.constants import (
    MIN_LEN_PASSWORD,
    MAX_LEN_PASSWORD,
    MIN_ID,
    MAX_ID,
)
from core.utils import checking_simple_types


def validate_string_by_pattern(
    string: str,
    pattern: re.Pattern,
    allow_empty: bool = True,
) -> bool:
    if allow_empty and string == '':
        return True
    return re.match(pattern, string) is not None


@checking_simple_types(type_to_check=int, field_name='id')
def check_field_id_is_valid(value: int) -> bool:
    """
    Проверяет корректность id для любой сущности приложения.
    :param value: Натуральное число в диапазоне {1, 32000}
    :return: True если _id валидный иначе False.
    """
    return MIN_ID <= value <= MAX_ID


@checking_simple_types(type_to_check=str, field_name='firstname')
def check_firstname_is_valid(value: str) -> bool:
    """
    Проверяет валидность firstname.
    :param value: Строка firstname.
    :return: True or False.
    """
    return validate_string_by_pattern(value, FIRST_NAME_PATTERN)


@checking_simple_types(type_to_check=str, field_name='lastname')
def check_lastname_is_valid(value: str) -> bool:
    """
    Проверяет валидность lastname.
    :param value: Строка lastname.
    :return: True or False.
    """
    return validate_string_by_pattern(value, LAST_NAME_PATTERN)


@checking_simple_types(type_to_check=str, field_name='username')
def check_username_is_valid(value: str) -> bool:
    """
    Проверяет валидность username.
    :param value: Строка username.
    :return: True or False.
    """
    return validate_string_by_pattern(value, USERNAME_PATTERN, allow_empty=False)


@checking_simple_types(type_to_check=str, field_name='email')
def check_email_is_valid(value: str) -> bool:
    """
    Проверяет валидность email.
    :param value: Строка email.
    :return: True or False.
    """
    return validate_string_by_pattern(value, EMAIL_PATTERN)


@checking_simple_types(type_to_check=bytes, field_name='password')
def check_password_is_valid(value: bytes) -> bool:
    """
    Проверяет валидность password.
    :param value: Строка password.
    :return: True or False.
    """
    return len(value) > 2


@checking_simple_types(type_to_check=str, field_name='phone_number')
def check_phone_number_is_valid(value: str) -> bool:
    """
    Проверяет валидность phone_number.
    :param value: Строка phone_number.
    :return: True or False.
    """
    return validate_string_by_pattern(value, PHONE_NUMBER_PATTERN)


@checking_simple_types(type_to_check=str, field_name='telegram')
def check_telegram_is_valid(value: str) -> bool:
    """
    Проверяет валидность telegram.
    :param value: Строка telegram.
    :return: True or False.
    """
    if value == '':
        return True
    return value.startswith('@')


@checking_simple_types(type_to_check=str, field_name='description')
def check_description_is_valid(value: str) -> bool:
    """
    Проверяет валидность description.
    :param value: Строка description.
    :return: True or False.
    """
    return len(value) < 255


def check_is_valid_enum(enum_cls: type[Enum], value: Any) -> bool:
    """
    Проверяет валидность value. Объект value должен быть
    членом класса enum_cls.
    :param enum_cls: Enum или его подтип.
    :param value: Член класса enum_cls".
    :return: True or False.
    """
    try:
        enum_cls(value)
    except ValueError:
        raise TypeError(f'{value!r} must be an {enum_cls.__name__!r}')
    return True


@checking_simple_types(type_to_check=str, field_name='password')
def check_set_password(value: str) -> bool:
    """
    Проверяет валидность устанавливаемого password.
    :param value: Строка password.
    :return: True or False.
    """
    return validate_string_by_pattern(value, PASSWORD_PATTERN, allow_empty=False)


# def validate_field_id(value: int, check_type: bool = True) -> bool:
#     if check_type and not isinstance(value, int):
#         raise TypeError(f'id must be an {int!r}')
#     if not validate_id(value):
#         return False
#     return True
#
#
# def validate_field_email(value: str, check_type: bool = True) -> bool:
#     if check_type and not isinstance(value, str):
#         raise TypeError(f'email must be an {str!r}')
#     if not value != '' and validate_email(value) is False:
#         return False
#     return True
