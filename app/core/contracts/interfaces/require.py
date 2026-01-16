from collections.abc import Container, Callable
from typing import Protocol, runtime_checkable, Any


@runtime_checkable
class ContractRequireProtocol(Protocol):

    handler: Callable[..., bool]
    contract: str
    violation: str
    detail: str
    custom_exception: Exception | type[Exception] | None
    environments: Container[str] | None

    def __call__(self, *args, **kwargs) -> bool: ...


@runtime_checkable
class ContractProcessValueRequireProtocol(ContractRequireProtocol, Protocol):

    handler:  Callable[[Any], Any]

    def __call__(self, *args, **kwargs) -> Any: ...
