from pydantic import BaseModel, field_validator
from pydantic_core import ValidationError


class A(BaseModel):
    id: int
    name: str


class Exc(ValueError):
    pass

try:
    a = A(id=1, name=2)
except ValidationError as e:
    print(e)

if __name__ == '__main__':
    pass