from collections.abc import Callable
from functools import wraps

import bcrypt


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


# def gen_password(
#     min_length: int = 3,
#     max_length: int = 20,
# ) -> str:
#     chars = string.ascii_letters + string.digits + string.punctuation
#     return ''.join(
#         secrets.choice(chars) for _ in range(random.randint(min_length, max_length))
#     )
