from collections.abc import Callable, Iterable, Container

from core.contracts.interfaces.require import ContractRequireProtocol


AcceptRequireTypeAsTuple = (
    tuple[
        Callable[..., bool] | Callable[[], bool],
        str,
        str,
        Exception | type[Exception] | None,
        Container[str] | None
    ]
)


AcceptRequireType = Iterable[
    ContractRequireProtocol | Callable[..., bool] | AcceptRequireTypeAsTuple
]

AcceptTypesCreateRequire = ContractRequireProtocol | Callable[..., bool] | AcceptRequireTypeAsTuple