import json
from datetime import datetime
from typing import Any

# from .error_codes import ErrorData
from core.error_codes import ErrorData


class BaseAppError(Exception):
    """
    Базовое исключение домена.
    Все доменные исключения должны наследоваться от него.
    """
    code: str = ErrorData.INTERNAL_ERROR.code
    message: str = ErrorData.INTERNAL_ERROR.message
    http_status: int = ErrorData.INTERNAL_ERROR.http_status_code

    def __init__(
        self,
        *,
        message: str| None = None,
        code: str| None = None,
        context: dict[str, Any] | None = None,
        **kwargs
    ):
        self.message = message or self.message
        self.code = code or self.code
        self.context = context or {}
        self.context.update(kwargs)
        self.timestamp = datetime.now().isoformat()
        super().__init__(self.message)

    def to_dict(self) -> dict[str, Any]:
        """Сериализация исключения в словарь."""
        return {
            "code": self.code,
            "message": self.message,
            "details": self.details,
            "timestamp": self.timestamp,
            "exception_type": self.__class__.__name__
        }

    def to_json(self, indent=None, ensure_ascii=False) -> str:
        """Сериализация исключения в JSON."""
        return json.dumps(
            self.to_dict(),
            indent=indent,
            ensure_ascii=ensure_ascii,
        )

    def __str__(self) -> str:
        return f"[{self.code}] {self.message}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(code={self.code!r}, message={self.message!r})"

if __name__ == '__main__':
    print(ErrorData.INTERNAL_ERROR.code)
    print(ErrorData.INTERNAL_ERROR.message)
    print(ErrorData.INTERNAL_ERROR.http_status_code)