from collections import ChainMap
from dataclasses import dataclass, astuple
from datetime import datetime
from enum import Enum
from types import UnionType, NoneType
from typing import (
    Annotated,
    Type,
    Union,
    get_type_hints,
    get_args,
    get_origin,
    Protocol,
    Any,
)

from pydantic import (
    BaseModel,
    BeforeValidator,
    ConfigDict,
    EmailStr,
    Field,
    field_validator,
)

s1 = {"1", "2"}
s3 = {"1", "2", "4", "5"}


def bar(x: int | None) -> None:
    print(get_type_hints(bar))
    print(locals())
    print(bar.__annotations__)


cm = ChainMap({1: "1"}, {2: "2", 1: "1"})

FieldName = Annotated[str, "Имя поля. Не должно быть пустым и превышать 100 символов."]

class E(Enum):
    x = 1



if __name__ == "__main__":
    origin = get_origin(FieldName)
    args = get_args(FieldName)
    print(isinstance(str | int, UnionType))
    print(issubclass(E, Enum))
