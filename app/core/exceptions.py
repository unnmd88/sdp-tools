import json
from datetime import datetime
from typing import Any

# from .error_codes import ErrorData
from core.error_data import ErrorData


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
        message: str | None = None,
        code: str | None = None,
        subject: str | None = None,
        context: dict[str, Any] | None = None,
        **kwargs,
    ):
        self.message = message or self.message
        self.code = code or self.code
        self.subject = subject
        self.context = (context or {}) | kwargs
        self.timestamp = datetime.now().isoformat()
        super().__init__(self.message)

    def to_dict(self) -> dict[str, Any]:
        """Сериализация исключения в словарь."""
        return {
            "code": self.code,
            "message": self.message,
            "subject": self.subject,
            "context": self.context,
            "timestamp": self.timestamp,
            "exception_type": self.__class__.__name__,
        }

    def __str__(self) -> str:
        return f"[{self.code}] subject={self.subject!r} {self.message}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(code={self.code!r} subject={self.subject!r} message={self.message!r})"


if __name__ == "__main__":
    print(ErrorData.INTERNAL_ERROR.code)
    print(ErrorData.INTERNAL_ERROR.message)
    print(ErrorData.INTERNAL_ERROR.http_status_code)
