from dataclasses import dataclass, astuple
from datetime import datetime
from types import UnionType
from typing import Annotated, Type, Union

from pydantic import(
    BaseModel,
    BeforeValidator,
    ConfigDict,
    EmailStr,
    Field,
    field_validator,
)

s1 = {"1", "2"}
s3 = {"1","2","4","5"}


def decorator(func):
    def foo(*args, **kwargs):
        arg_names = func.__code__.co_varnames
        print(arg_names)
        return func(*args, **kwargs)
    return foo


@decorator
def bar(a: str | None):
    print('bar. arg a: ', a, ' type: ', type(a), ' value: ', a)

dtm = datetime.now()


if __name__ == '__main__':
    bar(None)
    print(isinstance(dtm, int))
