"""
Модуль, содержащий базовые исключения.
"""

import datetime
import json
from typing import Any

from core.http_codes import HTTP_500_INTERNAL_SERVER_ERROR
from core.error_codes import ErrorCodes


class ApplicationError(Exception):
    """Ошибка приложения."""





class DomainError(ApplicationError):
    """
    Базовое исключение домена.
    Все доменные исключения должны наследоваться от него.
    """

    code: str = ErrorCodes.DOMAIN_ERROR
    message: str = ErrorCodes.DOMAIN_ERROR
    http_status: int = HTTP_500_INTERNAL_SERVER_ERROR

    def __init__(
        self,
        *,
        message: str | None = None,
        code: str | None = None,
        detail: str = None,
    ):
        self.message = message or self.message
        self.code = code or self.code
        self.detail = detail or self.message
        self.timestamp = datetime.now().isoformat()
        super().__init__(self.detail)

    def to_dict(self) -> dict[str, Any]:
        """Сериализация исключения в словарь."""
        return {
            "code": self.code,
            "message": self.message,
            "detail": self.detail,
            "timestamp": self.timestamp,
            "exception_type": self.__class__.__name__,
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
        return (
            f"{self.__class__.__name__}("
            f"code={self.code!r} "
            f"message={self.message!r} "
            f"detail={self.detail!r}"
            f")"
        )
