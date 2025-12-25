from dataclasses import dataclass, astuple


@dataclass
class A:
    f: int
    b: str

if __name__ == '__main__':
    x = A(1, 'eqew')
    print(astuple(x))