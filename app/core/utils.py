import random
import re
import secrets
import string
from collections.abc import Callable, Iterable
from functools import wraps
from types import UnionType
from typing import TYPE_CHECKING

from dataclasses import asdict


if TYPE_CHECKING:
    pass


def checking_types(
    *,
    isinstance_of: type | UnionType | Iterable[type],
    field_name_for_exception: str = 'field_name',
):
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
    :param isinstance_of: Тип или объединение типов для проверки.
    :param field_name_for_exception: Название поля для вывода текста ошибки.
    """
    if isinstance(isinstance_of, Iterable):
        isinstance_of = tuple(isinstance_of)
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(value, *args, **kwargs):
            if not isinstance(value, isinstance_of):
                raise TypeError(f'{field_name_for_exception!r} value must be an instance of {isinstance_of!r}')
            return func(value, *args, **kwargs)
        return wrapper
    return decorator


def validate_string_by_pattern(
    string_to_validate: str,
    pattern: re.Pattern,
    allow_empty: bool = True,
) -> bool:
    if allow_empty and string_to_validate == '':
        return True
    return re.match(pattern, string_to_validate) is not None


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


@checking_types(isinstance_of=str | set)
def foo(value):
    print(value)


if __name__ == '__main__':
    foo('1')
    foo([2])
