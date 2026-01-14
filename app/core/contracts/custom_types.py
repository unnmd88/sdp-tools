from collections.abc import Callable, Iterable

from core.contracts.interfaces.require import ContractRequireProtocol

AcceptRequireTypeAsTuple = tuple[Callable[..., bool] | Callable[[], bool], str, Exception | type[Exception] | None]

AcceptRequireType = Iterable[
    ContractRequireProtocol | Callable[..., bool] | AcceptRequireTypeAsTuple
]

AcceptTypesCreateRequire = ContractRequireProtocol | Callable[..., bool] | AcceptRequireTypeAsTuple