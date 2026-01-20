from collections.abc import Container, Callable
from typing import Protocol, runtime_checkable, Any


@runtime_checkable
class ContractRequireSchemaProtocol(Protocol):
    handler: Callable[..., bool]
    metadata: Any = None
    custom_exception: Exception | type[Exception] | None
    environments: Container[str] | None

    def __call__(self, *args, **kwargs) -> bool: ...

    def to_dict(self) -> dict[str, Any]:
        return {
            "handler": self.handler.__name__,
            "metadata": self.metadata,
            "custom_exception": self.custom_exception.__class__.__name__
            if self.custom_exception
            else None,
            "environments": self.environments,
        }


@runtime_checkable
class ContractProcessValueSchemaRequireProtocol(
    ContractRequireSchemaProtocol, Protocol
):
    handler: Callable[[Any], Any]

    def __call__(self, *args, **kwargs) -> Any: ...
