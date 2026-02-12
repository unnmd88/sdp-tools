import re
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
    field_name_for_exception: str = "field_name",
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
                raise TypeError(
                    f"{field_name_for_exception!r} value must be an instance of {isinstance_of!r}"
                )
            return func(value, *args, **kwargs)

        return wrapper

    return decorator


def validate_string_by_pattern(
    string_to_validate: str,
    pattern: re.Pattern,
    allow_empty: bool = True,
) -> bool:
    if allow_empty and string_to_validate == "":
        return True
    return re.match(pattern, string_to_validate) is not None


if __name__ == "__main__":
    foo("1")
    foo([2])
