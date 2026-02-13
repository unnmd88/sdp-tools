from collections.abc import Sequence
from dataclasses import is_dataclass

from typing import Any, Self

from core.enums import ContextKey
from core.error_codes import ErrorCodes


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
        request_id: str | None = None,
        context: dict[str, Any] = None,
        **kwargs,
    ):
        self._private_message = private_message or self.DEFAULT_PRIVATE_MESSAGE
        self._public_message = public_message or self.DEFAULT_PUBLIC_MESSAGE
        self._code = code or self.DEFAULT_CODE
        self._context = context if context is not None else {}
        self._extra = kwargs or {}
        self._request_id = request_id
        super().__init__(self._private_message)

    def to_dict(self) -> dict[str, Any]:
        """Сериализация исключения в словарь."""

        return {
            "code": self._code,
            "request_id": self._request_id,
            "private_message": self._private_message,
            "public_message": self._public_message,
            "context": self._context,
            "exception_type": self.__class__.__name__,
            "extra": self.extra,
        }

    def _keys_to_str(self, to_update: dict) -> Sequence[tuple[str, Any]]:
        return [(str(k), v) for k, v in to_update.items()]

    def _with_context_by_dict(self, to_update: dict) -> Self:
        """Универсальный метод для добавления контекста."""
        self._context.update(self._keys_to_str(to_update))
        return self

    def with_context(self, **kwargs) -> Self:
        """Универсальный метод для добавления контекста."""
        self._context.update(self._keys_to_str(kwargs))
        return self

    def with_request_id(self, request_id: str) -> Self:
        """Добавляет ID запроса."""
        return self.with_context(request_id=request_id)

    def with_entity_context(
        self,
        *,
        entity: type,
        entity_id: str | int = None,
    ) -> Self:
        """Добавляет контекст сущности."""
        self._with_context_by_dict({
            ContextKey.ENTITY_NAME: entity.__name__,
            ContextKey.ENTITY_ID: entity_id,
        })
        return self

    def with_handler_context(self, handler: Any) -> Self:
        self._with_context_by_dict({ContextKey.HANDLER: handler})
        return self

    def with_action_context(self, action: Any) -> Self:
        self._with_context_by_dict({ContextKey.ACTION: action})
        return self

    def update_context(
        self, other: dict[str, Any]
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
    def context(self) -> dict[str, Any]:
        return self._context

    def __str__(self) -> str:
        return f"[{self._code}] {self._private_message}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(code={self._code!r} message={self._private_message!r})"


if __name__ == "__main__":
    print(ErrorCodes.INTERNAL_ERROR.code)
    print(ErrorCodes.INTERNAL_ERROR.private_message)
