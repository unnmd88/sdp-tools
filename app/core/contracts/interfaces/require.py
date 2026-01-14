from collections.abc import Container, Callable
from typing import Protocol, runtime_checkable


@runtime_checkable
class ContractRequireProtocol(Protocol):

    predicate: Callable[..., bool] | Callable[[], bool]
    description: str
    custom_exception: Exception | type[Exception] | None
    environments: Container[str]

    def __call__(self, value, **kwargs): ...

