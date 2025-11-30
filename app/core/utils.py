from collections.abc import Callable
from enum import Enum
from functools import wraps


def type_validator(*, type_to_check: type, field_name: str = ''):
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(value, *args, **kwargs):
            if issubclass(type_to_check, Enum):
                try:
                    type_to_check(value)
                except ValueError:
                    raise TypeError(
                        f'{field_name!r} must be an {type_to_check.__name__!r}'
                    )
            else:
                if not isinstance(value, type_to_check):
                    raise TypeError(f'{field_name!r} must be an {type_to_check.__name__!r}')
            return func(value, *args, **kwargs)
        return wrapper
    return decorator



