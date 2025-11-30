from dataclasses import dataclass, asdict, astuple


@dataclass
class A:
    id: int
    name: str
    manes: list[str]



def check_types_from_dataclass_instance(dataclass_instance):
    instance_types = dataclass_instance.__annotations__
    for field_name, field_type in instance_types.items():
        if not isinstance(field_type, instance_types[field_name]):
            pass


if __name__ == '__main__':
    a = A(id=1, name='test', manes=['dasd', '3333'])
    print(isinstance(a.id, a.__annotations__['id']))
    print(a.__annotations__)
    print(asdict(a))
    print(astuple(a))
