from collections.abc import Callable
from typing import get_origin, Annotated, Any, get_args

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


if __name__ == "__main__":
    o = Annotated[int, "Abra", "CAdabra"]
    print(to_annotated(o))
    o1 = lambda x: x
    print(to_annotated(o1))
