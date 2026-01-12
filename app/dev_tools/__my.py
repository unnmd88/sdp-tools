from collections import ChainMap
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


cm = ChainMap({1: '1'}, {2: '2', 1: '1'})

if __name__ == '__main__':
    print(cm)
    print(cm.pop(1))
    print(cm)
    print(cm.pop(1))
    print(cm)

    try:
        v = int([])
    except TypeError as e:
        print(e)
