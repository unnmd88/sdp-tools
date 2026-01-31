from dataclasses import dataclass
from typing import TypeVar, NoReturn

from core.exceptions import BaseAppError

E = TypeVar("E", bound=BaseAppError)


@dataclass(kw_only=True, frozen=True, slots=True)
class Result[T, E]:

    value: T | None = None
    error: E | None = None

    @classmethod
    def success(cls, value: T) -> "Result[T, NoReturn]":
        return cls(value=value)

    @classmethod
    def failure(cls, error: E) -> "Result[NoReturn, E]":
        return cls(error=error)

    @property
    def is_ok(self) -> bool:
        return self.value is not None

    @property
    def is_err(self) -> bool:
        return self.error is not None

    def unwrap(self) -> T:
        if self.is_ok:
            return self.value
        else:
            raise self.error


if __name__ == '__main__':
    r = Result.success(1)
    r1 = Result.failure(BaseAppError())
    print(r)
    print(r1)