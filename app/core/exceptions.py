import json
from dataclasses import dataclass, is_dataclass, asdict
from datetime import datetime
from typing import Any, Protocol, runtime_checkable, ClassVar
from typing import dataclass_transform

# from .error_codes import ErrorData
from core.error_data import ErrorData


class ErrorContextAsAnyDataclassProtocol(Protocol):
    """Protocol для аннотации любого dataclass экземпляра"""

    __dataclass_fields__: ClassVar[dict]
    __dataclass_params__: ClassVar[Any]


class BaseAppError(Exception):
    """
    Базовое исключение домена.
    Все доменные исключения должны наследоваться от него.
    """

    DEFAULT_CODE: str = ErrorData.INTERNAL_ERROR.code
    DEFAULT_MESSAGE: str = ErrorData.INTERNAL_ERROR.message

    def __init__(
        self,
        *,
        message: str | None = None,
        code: str | None = None,
        context: ErrorContextAsAnyDataclassProtocol | dict[str, Any] | None = None,
        **kwargs,
    ):
        self.message = message or self.DEFAULT_MESSAGE
        self.code = code or self.DEFAULT_CODE
        self.context = context
        self.extra = kwargs or {}
        super().__init__(self.message)

    def to_dict(self) -> dict[str, Any]:
        """Сериализация исключения в словарь."""
        if is_dataclass(self.context):
            ctx = asdict(self.context)
        else:
            ctx = self.context or {}
        return {
            "code": self.code,
            "message": self.message,
            "context": ctx,
            "exception_type": self.__class__.__name__,
            "extra": self.extra,
        }

    def update_context(self, other: ErrorContextAsAnyDataclassProtocol | dict[str, Any]):
        if is_dataclass(other):
            self.context = other
        elif isinstance(other, dict):
            self.context |= other

    def __str__(self) -> str:
        return f"[{self.code}] {self.message}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(code={self.code!r} message={self.message!r})"





if __name__ == "__main__":
    print(ErrorData.INTERNAL_ERROR.code)
    print(ErrorData.INTERNAL_ERROR.message)
    print(ErrorData.INTERNAL_ERROR.http_status_code)
