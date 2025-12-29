from collections.abc import Callable, Container
from functools import wraps
from typing import TYPE_CHECKING

import bcrypt

from dataclasses import asdict
from core.enums import Permissions
from core.exceptions.base import PermissionsError


if TYPE_CHECKING:
    from _typeshed import DataclassInstance


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


def check_permissions_async(*permissions_to_check: Permissions):
    permissions_to_check: frozenset[Permissions] = frozenset(permissions_to_check)

    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            self = args[0]
            if not permissions_to_check.issubset(
                self.user_entity.permissions.get_all()
            ):
                raise PermissionsError
            return await func(*args, **kwargs)

        return wrapper

    return decorator


def hash_password(
    password: str,
) -> bytes:
    return bcrypt.hashpw(
        password.encode('utf-8'),
        bcrypt.gensalt(),
    )


def validate_password(
    password: str,
    hashed_password: bytes,
) -> bool:
    return bcrypt.checkpw(
        password=password.encode('utf-8'),
        hashed_password=hashed_password,
    )


def not_none_dataclass_instance_attrs_to_dict(
    dataclass_instance,
    default_exclude_fields: frozenset | set | None = frozenset(('id', '_id', 'filters_for_search')),
    *exclude_fields,
) -> dict:
    exclude = default_exclude_fields or frozenset()
    if exclude_fields:
        exclude = exclude | frozenset(exclude_fields)
    return {
        k: v for k, v in asdict(dataclass_instance).items()
        if v is not None and k not in exclude
    }





#    return {
#    asdict(dataclass_instance)
# }
# def gen_password(
#     min_length: int = 3,
#     max_length: int = 20,
# ) -> str:
#     chars = string.ascii_letters + string.digits + string.punctuation
#     return ''.join(
#         secrets.choice(chars) for _ in range(random.randint(min_length, max_length))
#     )

