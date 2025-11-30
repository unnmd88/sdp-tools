from dataclasses import dataclass, field, asdict, astuple
from enum import StrEnum, Enum
from typing import Annotated, final

from pydantic import BaseModel, field_validator
from pydantic_core import ValidationError

def df(num: int):
    if not isinstance(num, int):
        raise TypeError
    return 234


@final
@dataclass
class A:
    id: Annotated[int, field(default_factory=df)]
    name: str = ''



class E(StrEnum):
    a = 'A'

if __name__ == '__main__':
    a = A(id=1, name='test')
    # print(isinstance(a.id, a.__annotations__['id']))
    print(a.__annotations__)
    print(asdict(a))
    print(astuple(a))
    print(f'{list[str]!r}')

    e = E(1)
    print(isinstance(e, Enum))

