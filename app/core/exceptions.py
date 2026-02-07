import json
from dataclasses import dataclass, is_dataclass, asdict
from datetime import datetime
from typing import Any, Protocol, runtime_checkable, ClassVar
from typing import dataclass_transform

# from .error_codes import ErrorData
from core.error_codes import ErrorCodes


class ErrorContextAsAnyDataclassProtocol(Protocol):
    """Protocol для аннотации любого dataclass экземпляра"""

    __dataclass_fields__: ClassVar[dict]
    __dataclass_params__: ClassVar[Any]


class BaseAppError(Exception):
    """
    Базовое исключение домена.
    Все доменные исключения должны наследоваться от него.
    """

    DEFAULT_CODE: str = ErrorCodes.INTERNAL_ERROR.code
    DEFAULT_PRIVATE_MESSAGE: str = ErrorCodes.INTERNAL_ERROR.private_message
    DEFAULT_PUBLIC_MESSAGE: str = ErrorCodes.INTERNAL_ERROR.private_message

    def __init__(
        self,
        *,
        private_message: str | None = None,
        public_message: str | None = None,
        code: str | None = None,
        context: ErrorContextAsAnyDataclassProtocol | dict[str, Any] | None = None,
        **kwargs,
    ):
        self._private_message = private_message or self.DEFAULT_PRIVATE_MESSAGE
        self._public_message = public_message or self.DEFAULT_PUBLIC_MESSAGE
        self._code = code or self.DEFAULT_CODE
        self._context = context
        self._extra = kwargs or {}
        super().__init__(self._private_message)

    def to_dict(self) -> dict[str, Any]:
        """Сериализация исключения в словарь."""
        if is_dataclass(self._context):
            ctx = asdict(self._context)
        else:
            ctx = self._context or {}
        return {
            "code": self._code,
            "private_message": self._private_message,
            "public_message": self._public_message,
            "context": ctx,
            "exception_type": self.__class__.__name__,
            "extra": self.extra,
        }

    def update_context(
        self, other: ErrorContextAsAnyDataclassProtocol | dict[str, Any]
    ):
        if is_dataclass(other):
            self._context = other
        elif isinstance(other, dict):
            self._context |= other

    @property
    def extra(self) -> dict[str, Any]:
        return self._extra

    @property
    def private_message(self) -> str:
        return self._private_message

    @property
    def public_message(self) -> str:
        return self._public_message

    @property
    def context(self) -> ErrorContextAsAnyDataclassProtocol | dict[str, Any]:
        return self._context

    def __str__(self) -> str:
        return f"[{self._code}] {self._private_message}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(code={self._code!r} message={self._private_message!r})"


if __name__ == "__main__":
    print(ErrorCodes.INTERNAL_ERROR.code)
    print(ErrorCodes.INTERNAL_ERROR.private_message)
    print(ErrorCodes.INTERNAL_ERROR.http_status_code)
