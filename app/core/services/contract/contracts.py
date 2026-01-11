from collections.abc import Callable, Iterable
from functools import wraps
from types import UnionType
from typing import NamedTuple, Sequence, TypeAlias, Union, Type, TypeVar, Any, get_type_hints

from core.exceptions.base import DomainValidationError, DomainTypeValidationError
from core.exceptions.contract import ContractViolationError
from core.services.type_cheker import TypeChecker

TA_Preconditions: TypeAlias = tuple[Iterable[tuple[Callable[..., bool], str]], type[DomainValidationError]]
type T_ToCheck = type | tuple[type, ...] | UnionType


class ContractRequire(NamedTuple):
    predicate: Callable[..., bool] | Callable[[], bool]
    exception: ContractViolationError = ContractViolationError


class ContractConditions(NamedTuple):
    """Контейнер для условий валидации значения в контракте.

    Используется для определения предусловий, которые должны быть выполнены
    при проверке корректности значения (например, в валидаторах доменных объектов).
    В случае, если одно из условий не выполняется, выбрасывается указанное исключение
    с соответствующим сообщением об ошибке.

    Attrs:
        requires (Sequence[tuple[Callable[..., bool], str]]):
            Последовательность кортежей, где каждый кортеж содержит:
                - Функцию-предикат, принимающую аргументы и возвращающую bool.
                  Если функция возвращает False, контракт считается нарушенным.
                - Строка — пользовательское сообщение об ошибке для этого условия.

        exception (type[DomainValidationError], опционально):
            Тип исключения, которое будет возбуждено при нарушении условий.
            Должен быть подклассом DomainValidationError.
            По умолчанию — DomainValidationError.
    Raises:
        DomainValidationError: Если указан недопустимый тип исключения.
    """
    requires: Sequence[ContractRequire]
    exception: type[ContractViolationError] = ContractViolationError


def contract(
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
                TypeChecker.vector_types_check(locals_args=_locals, annotations=type_hints)
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



class Foo:
    def __init__(self, value: str):
        self.value = value
        print(f'Foo1: {value}')

    @contract(
        checking_types_of_args=False,
        checking_return_type=False,
        has_self=True,
        # type_check=str | None,
        preconditions=ContractConditions(
            requires=(
                        (lambda x: len(x) > 3, "Слишком короткий username"),
                        (lambda x: len(x) < 16, "Слишком длинный username")
                     )
            ),
        # field_name='username',
    )
    def set_username(self, value: str):
        self.value = value
        print(f'Foo2: {value}')


@contract(
    checking_types_of_args=False,
    checking_return_type=False,
    has_self=False,
    # type_check=(str, ),
    preconditions=ContractConditions(
        requires=(
                    (lambda x: len(x) > 3, "Слишком короткий username"),
                    (lambda x: len(x) < 16, "Слишком длинный username")
                 )
        ),
    # field_name='bAr',
    )
def bar(value: str):
    print(f'bar: {value}')


if __name__ == '__main__':
    pass
    # o = Foo('first')
    # o.set_username('second')
    # bar(1)