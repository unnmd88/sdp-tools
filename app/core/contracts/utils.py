import inspect
from collections.abc import Iterable
from typing import get_origin, Annotated, Any, get_args, Protocol, Callable

from core.contracts.custom_types import AcceptRequireType, AcceptTypesCreateRequire
from core.contracts.interfaces.require import ContractRequireProtocol

from core.contracts.requires import ContractRequire


def to_annotated(
    value: Callable | Annotated[Callable, str, ...],
) -> Annotated[Callable, str]:
    is_annotated = get_origin(value)
    if not (is_annotated is Annotated):
        as_annotated = Annotated[value, ""]
    else:
        as_annotated = value
    args = get_args(as_annotated)
    if len(args) < 2:
        raise ValueError(
            f"Ожидается Annotated с двумя или более позициями. Получено {value!r}"
        )
    if not callable(args[0]):
        raise ValueError(
            f"Ожидается Annotated с вызываемым объектом в первой позиции. Получено {value!r}."
            f"Annotated-объект: {as_annotated!r}"
        )
    assert get_origin(as_annotated) is Annotated, "Должен быть Annotated(Ошибка в коде)"
    assert len(get_args(as_annotated)) >= 2, (
        "Должен быть Annotated с двумя или более позициями. Ошибка в коде"
    )
    return as_annotated


def get_contract_require(
    *,
    obj: ContractRequire | Callable[..., bool],
    attr_name_for_raise_detail: str,
    description: str = "",
) -> ContractRequire | Callable[..., bool]:
    if isinstance(obj, ContractRequire):
        return obj
    if callable(obj):
        return ContractRequire(
            predicate=obj,
            description=description,
        )
    raise TypeError(
        f"Передан невалидный объект-зависимости."
        f"Допускается только {ContractRequire.__name__!r} или сallable-объект. "
        f"Получен {obj!r}. Имя атрибута: {attr_name_for_raise_detail!r}."
    )


class TestProtocol(Protocol):
    def __call__(self, x: int) -> int: ...
    one: int


class TestClas:
    cls_attr: int = 1

    def __init__(self, x):
        self.one = x
    def method(self): ...
    def __call__(self, x: int) -> int: ...


class ProtocolComplianceChecker:

    @classmethod
    def light_inspect(cls,*, obj: Any, protocol: type[Protocol]) -> Iterable[str]:
        """
         Проверяет соответствие протокола объекту.

        Args:
            obj:
            protocol:

        Returns: Список атрибутов, которые не соответствуют протоколу.

        """
        obj_attrs = set(attr for attr in dir(obj))

        missing_attrs = []
        for attr in cls._get_protocol_attrs(protocol):
            if attr not in obj_attrs:
                missing_attrs.append(attr)
        return missing_attrs

    @classmethod
    def _get_protocol_attrs(
        cls,
        obj: Any,
    ):
        for name, member in inspect.getmembers(obj):
            if name == '__protocol_attrs__':
                return member
        raise AttributeError(F"Не найден атрибут __protocol_attrs__ в {obj!r}")


def protocol_compliance_checker(obj: Any, protocol: type[Protocol]):
    report = {
        "ok": False,
        "missing_attrs": [],
        "missing_methods": [],
    }


if __name__ == "__main__":
    o = Annotated[int, "Abra", "CAdabra"]
    print(to_annotated(o))
    o1 = lambda x: x
    print(to_annotated(o1))
    print(ProtocolComplianceChecker.light_inspect(obj=TestClas(1), protocol=TestProtocol))


def create_contract_require(
    obj: AcceptTypesCreateRequire,
) -> ContractRequireProtocol:
    require = None
    if isinstance(obj, ContractRequireProtocol):
        require = obj
    elif callable(obj):
        require = ContractRequire(predicate=obj)
    elif isinstance(obj, tuple):
        if len(obj) != 3:
            raise TypeError(
                f"Кортеж должен содержать 3 элемента(передано{len(obj)}):\n"
                f"1) callable-объект(предикат)\n"
                f"2) str - описание ошибки\n"
                f"3) Exception - класс исключения(либо его экземпляр), либо None.\n"
                f"если None, то используется исключение по умолчанию.\n"
            )
        require = ContractRequire(predicate=obj[0], description=obj[1], custom_exception=obj[2])
    if require is None:
        arg_name = list(inspect.signature(create_contract_require).parameters)[0]
        raise TypeError(
            f"Некорректный тип аргумента {arg_name!r}={obj!r}'. "
            f"Аргумент должен соответствовать протоколу {ContractRequireProtocol.__name__!r} "
            f"или быть callable-объектом или кортежем из 3 элементов, где:\n"
            f"[0] -> callable-объект(предикат)\n"
            f"[1] -> str - описание ошибки\n"
            f"[2] -> Exception - класс исключения(либо его экземпляр), либо None.\n"
            f"если None, то используется исключение по умолчанию.\n"
        )
    assert isinstance(require, ContractRequireProtocol), (
        f"Не удалось создать экземпляр класса {ContractRequire.__name__!r}."
    )
    return require
