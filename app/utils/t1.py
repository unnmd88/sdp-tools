from typing import TypedDict


class MyDict(TypedDict):
    id: int
    name: str
    code: int


def foo(**kwargs):
    print(kwargs)


if __name__ == "__main__":
    d = MyDict(id=1)
    print(d)
    foo(**d)
