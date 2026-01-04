import random
import re
import secrets
import string
from collections.abc import Callable, Iterable
from functools import wraps
from typing import TYPE_CHECKING

from dataclasses import asdict
from core.enums import Permissions


if TYPE_CHECKING:
    pass


def checking_simple_types(*, type_to_check: type, field_name: str = ''):
    """
    Декоратор, проверяющий корректность типа объекта.
    Поддерживается проверка следующих типов для объекта value,
    переданного в параметр value функции wrapper:
        - int
        - str
        - list
        - tuple
        - dict
        - set
    :param type_to_check: Тип для проверки(int | str | list | tuple | dict | set)
    :param field_name: Название поля для вывода текста ошибки.
    """

    def decorator(func: Callable):
        @wraps(func)
        def wrapper(value, *args, **kwargs):
            if not isinstance(value, type_to_check):
                raise TypeError(f'{field_name!r} must be an {type_to_check.__name__!r}')
            return func(value, *args, **kwargs)

        return wrapper

    return decorator


def validate_string_by_pattern(
    string: str,
    pattern: re.Pattern,
    allow_empty: bool = True,
) -> bool:
    if allow_empty and string == '':
        return True
    return re.match(pattern, string) is not None


def not_none_dataclass_instance_attrs_to_dict(
    dataclass_instance,
    *exclude_fields,
    default_exclude_fields: frozenset | set | None = frozenset(('id', '_id', 'filters_for_search')),
) -> dict:
    exclude = default_exclude_fields or frozenset()
    if exclude_fields:
        exclude = exclude | frozenset(exclude_fields)
    return {
        k: v for k, v in asdict(dataclass_instance).items()
        if v is not None and k not in exclude
    }


def gen_password(
    min_length: int = 3,
    max_length: int = 20,
) -> str:
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(
        secrets.choice(chars) for _ in range(random.randint(min_length, max_length))
    )
