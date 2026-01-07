from enum import Enum
from typing import Any

from core.reg_exps import (
    EMAIL_PATTERN,
    FIRST_NAME_PATTERN,
    LAST_NAME_PATTERN,
    USERNAME_PATTERN,
    PHONE_NUMBER_PATTERN,
    NAME_TLO_PATTERN, DISTRICT_TLO_PATTERN, STREET_TLO_PATTERN,
)
from core.users.constants import (
    MIN_ID,
    MAX_ID,
)
from core.utils import checking_types, validate_string_by_pattern


@checking_types(isinstance_of=int | None, field_name_for_exception='id')
def check_field_id_is_valid(value: int) -> bool:
    """
    Проверяет корректность id для любой сущности приложения.
    :param value: Натуральное число в диапазоне {1, 32000}
    :return: True если _id валидный иначе False.
    """
    return MIN_ID <= value <= MAX_ID


@checking_types(isinstance_of=str | None, field_name_for_exception='firstname')
def check_firstname_is_valid(value: str) -> bool:
    """
    Проверяет валидность firstname.
    :param value: Строка firstname.
    :return: True or False.
    """
    return value is None or validate_string_by_pattern(value, FIRST_NAME_PATTERN)


@checking_types(isinstance_of=str | None, field_name_for_exception='lastname')
def check_lastname_is_valid(value: str) -> bool:
    """
    Проверяет валидность lastname.
    :param value: Строка lastname.
    :return: True or False.
    """

    return value is None or validate_string_by_pattern(value, LAST_NAME_PATTERN)


@checking_types(isinstance_of=str, field_name_for_exception='username')
def check_username_is_valid(value: str) -> bool:
    """
    Проверяет валидность username.
    :param value: Строка username.
    :return: True or False.
    """
    return 2 < len(value) < 32 and value.isalnum()


@checking_types(isinstance_of=str | None, field_name_for_exception='email')
def check_email_is_valid(value: str) -> bool:
    """
    Проверяет валидность email.
    :param value: Строка email.
    :return: True or False.
    """
    return value is None or validate_string_by_pattern(value, EMAIL_PATTERN)


@checking_types(isinstance_of=bytes, field_name_for_exception='password')
def check_password_is_valid(value: bytes) -> bool:
    """
    Проверяет валидность password.
    :param value: Строка password.
    :return: True or False.
    """
    return len(value) > 2


@checking_types(isinstance_of=str | None, field_name_for_exception='phone_number')
def check_phone_number_is_valid(value: str | None) -> bool:
    """
    Проверяет валидность phone_number.
    :param value: Строка phone_number.
    :return: True or False.
    """
    return value is None or validate_string_by_pattern(value, PHONE_NUMBER_PATTERN)


@checking_types(isinstance_of=str | None, field_name_for_exception='telegram')
def check_telegram_is_valid(value: str) -> bool:
    """
    Проверяет валидность telegram.
    :param value: Строка telegram.
    :return: True or False.
    """

    return value is None or (value.startswith('@') and (2 < len(value) < 32))


@checking_types(isinstance_of=str, field_name_for_exception='description')
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


# Блок проверки для Светофорного объекта(TrafficLightObjectEntity)

@checking_types(isinstance_of=str, field_name_for_exception='name')
def check_tlo_name_is_valid(value: str) -> bool:
    """
    Проверяет валидность name светофорного объекта.
    :param value: Строка name.
    :return: True or False.
    """
    return validate_string_by_pattern(value, NAME_TLO_PATTERN, allow_empty=False)


@checking_types(isinstance_of=str, field_name_for_exception='district')
def check_tlo_district_is_valid(value: str) -> bool:
    """
    Проверяет валидность district светофорного объекта.
    :param value: Строка district.
    :return: True or False.
    """
    return validate_string_by_pattern(value, DISTRICT_TLO_PATTERN, allow_empty=True)


@checking_types(isinstance_of=str, field_name_for_exception='street')
def check_tlo_street_is_valid(value: str) -> bool:
    """
    Проверяет валидность street светофорного объекта.
    :param value: Строка street.
    :return: True or False.
    """
    return validate_string_by_pattern(value, STREET_TLO_PATTERN, allow_empty=True)


@checking_types(isinstance_of=float, field_name_for_exception='latitude_or_longitude')
def check_tlo_latitude_or_longitude_is_valid(value: float) -> bool:
    """
    Проверяет валидность latitude_or_longitude светофорного объекта.
    :param value: Строка latitude_or_longitude.
    :return: True or False.
    """
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
