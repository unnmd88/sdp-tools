from collections.abc import Callable, Iterable, Container

from domain.contracts.interfaces.require_schemas_interfaces import (
    ContractRequireSchemaProtocol,
)


AcceptRequireTypeAsTuple = tuple[
    Callable[..., bool] | Callable[[], bool],
    str,
    str,
    Exception | type[Exception] | None,
    Container[str] | None,
]


AcceptRequireType = Iterable[
    ContractRequireSchemaProtocol | Callable[..., bool] | AcceptRequireTypeAsTuple
]

AcceptTypesCreateRequire = (
    ContractRequireSchemaProtocol | Callable[..., bool] | AcceptRequireTypeAsTuple
)
