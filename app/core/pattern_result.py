from collections.abc import Callable
from dataclasses import dataclass
from typing import TypeVar, NoReturn, Any

from core.exceptions import BaseAppError

T = TypeVar("T")
U = TypeVar("U")
E = TypeVar("E", bound=BaseAppError)


@dataclass(frozen=True, slots=True)
class Success[T]:
    """Контейнер для успешного результата"""

    value: T

    def map(self, func: Callable[[T], U]) -> "Success[U]":
        return Success(func(self.value))

    def bind(self, func: Callable[[T], "Result[U, E]"]) -> "Result[U, E]":
        return func(self.value)


@dataclass(frozen=True, slots=True)
class Failure[E]:
    error: E

    def unwrap(self) -> T:
        raise self.error


Result = Success[T] | Failure[E]


def is_ok(result: Result[T, E]) -> bool:
    return isinstance(result, Success)


def is_err(result: Result[T, E]) -> bool:
    return isinstance(result, Failure)


def unwrap(result: Result[T, E]) -> T:
    match result:
        case Success(value):
            return value
        case Failure(error):
            raise error


def unwrap_or(result: Result[T, E], default: T) -> T:
    match result:
        case Success(value):
            return value
        case Failure(_):
            return default


def unwrap_or_else(result: Result[T, E], f: Callable) -> T:
    match result:
        case Success(value):
            return value
        case Failure(error):
            return f(error)


if __name__ == "__main__":
    r = Success(1)
    r1 = Failure("Error")
    print(r)
    print(r1)
