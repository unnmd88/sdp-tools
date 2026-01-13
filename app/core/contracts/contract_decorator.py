from collections.abc import Callable
from functools import wraps
from types import UnionType
from typing import Sequence, get_type_hints
from typing_extensions import deprecated

from core.contracts import ContractRequire
from core.contracts.exc import ContractViolationError
from core.services.type_cheker import TypeChecker


def _contract_wrapper_factory(
    func: Callable,
    returns: type | tuple[type, ...] | UnionType,
    preconditions: Sequence[ContractRequire],
    postconditions: Sequence[ContractRequire],
    checking_types_of_args: bool,
    has_self: bool,
):
    args_exclude_self = slice(1 if has_self else 0, None)
    if checking_types_of_args:
        type_hints = get_type_hints(func)

        @wraps(func)
        def wrapper(*args, **kwargs):
            # Проверка типов входных параметров функции/метода
            if checking_types_of_args:
                if (_locals := kwargs.get("_locals")) is None:
                    raise AttributeError("Не передан словарь локальных переменных")
                TypeChecker.vector_types_check(
                    locals_args=_locals, annotations=type_hints
                )
            # Проверка предусловий
            for predicate, exception in preconditions:
                if not predicate(*args[args_exclude_self]):
                    raise exception or ContractViolationError
            result = func(*args)
            # Проверка типа возвращаемого значения
            if not isinstance(result, returns):
                raise TypeError(
                    f"Функция {func.__name__} должна возвращать {returns.__name__}, "
                    f"а не {type(result).__name__}."
                )
            # Проверка постусловий
            for predicate, exception in postconditions:
                if not predicate(*args[args_exclude_self]):
                    raise exception or ContractViolationError
            return result
    else:

        @wraps(func)
        def wrapper(*args, **kwargs):
            # Проверка предусловий
            for predicate, exception in preconditions:
                if not predicate(*args[args_exclude_self]):
                    raise exception or ContractViolationError
            print(f"DEBUG1: {func.__name__}")
            result = func(*args, **kwargs)
            # Проверка постусловий
            for predicate, exception in postconditions:
                if not predicate(*args[args_exclude_self]):
                    raise exception or ContractViolationError
            return result

    return wrapper


def contract(
    *,
    has_self: bool = True,
    checking_types_of_args: bool = False,
    preconditions: Sequence[ContractRequire] = None,
    postconditions: Sequence[ContractRequire] = None,
):
    preconditions = preconditions or ()
    postconditions = postconditions or ()

    def decorator(func):
        type_hints = get_type_hints(func)
        if (returns := type_hints.get("return")) is None and checking_types_of_args:
            raise AttributeError("Не указан тип возвращаемого значения")
        wrapper = _contract_wrapper_factory(
            func=func,
            returns=returns,
            preconditions=preconditions,
            postconditions=postconditions,
            checking_types_of_args=checking_types_of_args,
            has_self=has_self,
        )
        return wrapper

    return decorator


@deprecated("Используйте @contract")
def _contract(
    *,
    has_self: bool = True,
    checking_types_of_args: bool = False,
    checking_return_type: bool = False,
    preconditions: Sequence[ContractRequire] = None,
    postconditions: Sequence[ContractRequire] = None,
):
    args_exclude_self = slice(1 if has_self else 0, None)

    preconditions = preconditions or ()
    postconditions = postconditions or ()

    def decorator(func):
        type_hints = get_type_hints(func)
        if checking_return_type and (returns := type_hints.get("return")) is None:
            raise AttributeError("Не указан тип возвращаемого значения")

        @wraps(func)
        def wrapper(*args, **kwargs):
            # Проверка типов входных параметров функции/метода
            if checking_types_of_args:
                if (_locals := kwargs.get("_locals")) is None:
                    raise AttributeError("Не передан словарь локальных переменных")
                TypeChecker.vector_types_check(
                    locals_args=_locals, annotations=type_hints
                )
            # Проверка предусловий
            for predicate, exception in preconditions:
                if not predicate(*args[args_exclude_self]):
                    raise exception or ContractViolationError
            result = func(*args)
            # Проверка типа возвращаемого значения
            if checking_return_type and not isinstance(result, returns):
                raise TypeError(
                    f"Функция {func.__name__} должна возвращать {returns.__name__}, "
                    f"а не {type(result).__name__}."
                )
            # Проверка постусловий
            for predicate, exception in postconditions:
                if not predicate(*args[args_exclude_self]):
                    raise exception or ContractViolationError
            return result

        return wrapper

    return decorator


if __name__ == "__main__":
    print(isinstance(ContractViolationError(), ContractViolationError))
    # o = Foo('first')
    # o.set_username('second')
    # bar(1)
