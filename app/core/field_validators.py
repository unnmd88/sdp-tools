import re
from enum import Enum
from typing import Any

from core.enums.organizations import Organizations
from core.reg_exps import EMAIL_PATTERN, FIRST_NAME_PATTERN, LAST_NAME_PATTERN, USERNAME_PATTERN
from core.users.constants import MIN_LEN_PASSWORD, MAX_LEN_PASSWORD
from core.utils import type_validator


@type_validator(type_to_check=int, field_name='id')
def check_field_id_is_valid(value: int) -> bool:
    """
    Проверяет корректность id для любой сущности приложения.
    :param value: Натуральное число в диапазоне {1, 32000}
    :return: True если _id валидный иначе False.
    """
    return 1 <= value <= 32000


@type_validator(type_to_check=str, field_name='firstname')
def check_firstname_is_valid(value: str) -> bool:
    """
    Проверяет валидность firstname.
    :param value: Строка firstname.
    :return: True or False.
    """
    if value == '':
        return True
    return re.match(FIRST_NAME_PATTERN, value) is not None


@type_validator(type_to_check=str, field_name='lastname')
def check_lastname_is_valid(value: str) -> bool:
    """
    Проверяет валидность lastname.
    :param value: Строка lastname.
    :return: True or False.
    """
    if value == '':
        return True
    return re.match(LAST_NAME_PATTERN, value) is not None


@type_validator(type_to_check=str, field_name='username')
def check_username_is_valid(value: str) -> bool:
    """
    Проверяет валидность username.
    :param value: Строка username.
    :return: True or False.
    """
    return re.match(USERNAME_PATTERN, value) is not None


def check_organization_is_valid(value: Organizations) -> bool:
    """
    Проверяет валидность organization.
    :param value: Экземпляр класса Organizations.".
    :return: True or False.
    """
    try:
        Organizations(value)
    except ValueError:
        raise TypeError(
            f'{value!r} must be an {Organizations.__name__!r}'
        )
    return True


@type_validator(type_to_check=str, field_name='email')
def check_field_email_is_valid(value: str) -> bool:
    """
    Проверяет валидность email.
    :param value: Строка email.
    :return: True or False.
    """
    if value == '':
        return True
    return re.match(EMAIL_PATTERN, value) is not None


@type_validator(type_to_check=bytes, field_name='password')
def check_password_is_valid(value: bytes) -> bool:
    """
    Проверяет валидность password.
    :param value: Строка password.
    :return: True or False.
    """
    return MIN_LEN_PASSWORD <= len(value) <= MAX_LEN_PASSWORD


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
        raise TypeError(
            f'{value!r} must be an {enum_cls.__name__!r}'
        )
    return True





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




