from collections.abc import Callable, Iterable
from functools import wraps
from types import UnionType
from typing import NamedTuple, Sequence, TypeAlias, Union, Type, TypeVar

from core.users.exceptions import DomainValidationError, DominTypeValidationError

TA_Predicate: TypeAlias = tuple[Callable[..., bool], str]
TA_Preconditions: TypeAlias = tuple[Iterable[TA_Predicate], type[DomainValidationError]]
TA_Check: TypeAlias = tuple[type, ...] | UnionType
# class ContractExpectedType(NamedTuple):
#     """Конфигурация контракта для проверки ожидаемого типа данных.
#
#     Используется в декораторах контрактов, чтобы указать,
#     какие типы считаются валидными для входящего значения аргумента функции,
#     а также задать пользовательское  сообщение об ошибке при нарушении контракта.
#
#     Args:
#         expected (tuple[type, ...]): Кортеж из одного или нескольких типов, которые
#             считаются допустимыми. Проверка выполняется с помощью `isinstance()`.
#         err_message (str): Сообщение об ошибке, которое будет выброшено, если значение
#             не соответствует ни одному из указанных типов. По умолчанию — "Неверный тип данных".
#
#     Пример использования:
#         >>> contract = ContractExpectedType((str, ), "Ожидается строка")
#         >>> contract.expected
#         (<class 'str'>, )
#         >>> contract.err_message
#         'Ожидается строка'
#     """
#     expected: TA_Check
#     err_message: str = "Неверный тип данных"


class ContractConditions(NamedTuple):
    """Контейнер для условий валидации значения в контракте.

    Используется для определения предусловий, которые должны быть выполнены
    при проверке корректности значения (например, в валидаторах доменных объектов).
    В случае, если одно из условий не выполняется, выбрасывается указанное исключение
    с соответствующим сообщением об ошибке.

    Attrs:
        requires (Sequence[tuple[Callable[..., bool], str]], опционально):
            Последовательность кортежей, где каждый кортеж содержит:
                - Функцию-предикат, принимающую аргументы и возвращающую bool.
                  Если функция возвращает False, условие считается нарушенным.
                - Строка — пользовательское сообщение об ошибке для этого условия.
            По умолчанию — None (условия отсутствуют).

        exception (type[DomainValidationError], опционально):
            Тип исключения, которое будет возбуждено при нарушении условий.
            Должен быть подклассом DomainValidationError.
            По умолчанию — DomainValidationError.
    """
    requires: Sequence[tuple[Callable[..., bool], str]] = None
    exception: type[DomainValidationError] = DomainValidationError


def contract(
    *,
    has_self: bool = True,
    type_check: UnionType | type | Iterable[type]  = None,
    preconditions: ContractConditions | TA_Preconditions = None,
    postconditions: ContractConditions | TA_Preconditions = None,
    field_name: str = '',
    expected_types_as_str: str = '',
):
    if type_check is not None:
        if isinstance(type_check, UnionType):
            expected_types_as_str =  str(type_check).replace("|", "или")
        elif isinstance(type_check, Iterable):
            type_check = tuple(type_check)
            expected_types_as_str = " или ".join([t.__name__ for t in type_check])
        else:
            expected_types_as_str = type_check.__name__
    else:
        type_check = object

    if preconditions is None:
        preconditions = ContractConditions(requires=())
    elif isinstance(preconditions, ContractConditions):
        preconditions = preconditions
    else:
        preconditions = ContractConditions(*preconditions)
    if postconditions is None:
        postconditions = ContractConditions(requires=())
    elif isinstance(postconditions, ContractConditions):
        postconditions = postconditions
    else:
        postconditions = ContractConditions(*postconditions)
    value_index = 1 if has_self else 0

    def decorator(func):
        @wraps(func)
        def wrapper(*args):
            if not isinstance(value := args[value_index], type_check):
                raise DominTypeValidationError(field_name=field_name, expected=expected_types_as_str)
            for require, err_message in preconditions.requires:
                if not require(value):
                    raise preconditions.exception(err_message)
            result = func(*args)
            for require, err_message, exception in postconditions.requires:
                if not require(value):
                    raise preconditions.exception(err_message)
            return result
        return wrapper
    return decorator


class Foo:
    def __init__(self, value: str):
        self.value = value
        print(f'Foo1: {value}')

    @contract(
        has_self=True,
        type_check=str | None,
        preconditions=ContractConditions(
            requires=(
                        (lambda x: len(x) > 3, "Слишком короткий username"),
                        (lambda x: len(x) < 16, "Слишком длинный username")
                     )
            ),
        field_name='username',
    )
    def set_username(self, value: str):
        self.value = value
        print(f'Foo2: {value}')


@contract(
    has_self=False,
    type_check=(str, ),
    preconditions=ContractConditions(
        requires=(
                    (lambda x: len(x) > 3, "Слишком короткий username"),
                    (lambda x: len(x) < 16, "Слишком длинный username")
                 )
        ),
    field_name='bAr',
    )
def bar(value: str):
    print(f'bar: {value}')


if __name__ == '__main__':
    o = Foo('first')
    # o.set_username('second')
    bar(1)