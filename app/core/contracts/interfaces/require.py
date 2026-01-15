from collections.abc import Container, Callable
from dataclasses import dataclass
from typing import Protocol, runtime_checkable, Any


@runtime_checkable
class ContractRequireProtocol(Protocol):

    predicate: Callable[..., bool]
    contract: str
    violation: str
    detail: str
    custom_exception: Exception | type[Exception] | None
    environments: Container[str] | None

    def __call__(self, *args, **kwargs) -> bool: ...


@runtime_checkable
class ContractPreprocessRequireProtocol(ContractRequireProtocol, Protocol):

    # @property
    # def predicate(self) -> Callable[[Any], Any]: ...
    predicate:  Callable[[Any], Any]

    def __call__(self, *args, **kwargs) -> Any: ...
