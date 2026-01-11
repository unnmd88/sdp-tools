from dataclasses import dataclass, astuple
from datetime import datetime
from types import UnionType, NoneType
from typing import Annotated, Type, Union, get_type_hints

from pydantic import (
    BaseModel,
    BeforeValidator,
    ConfigDict,
    EmailStr,
    Field,
    field_validator,
)

s1 = {'1', '2'}
s3 = {'1', '2', '4', '5'}


def bar(x: int | None) -> None:
    print(get_type_hints(bar))
    print(locals())
    print(bar.__annotations__)


if __name__ == '__main__':
    try:
        v = int([])
    except TypeError as e:
        print(e)
