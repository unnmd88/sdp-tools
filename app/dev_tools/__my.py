from dataclasses import dataclass, astuple
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

def foo(union):
    # if not isinstance(union, UnionType):
    #     raise TypeError
    print(isinstance(None, union))


if __name__ == '__main__':
    foo(None | str)
    # foo(None)
    l1 = [int, str]

    print(Union(l1) == int | str)
