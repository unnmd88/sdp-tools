from dataclasses import dataclass, asdict
from datetime import datetime
from enum import StrEnum
from functools import cached_property
from typing import NamedTuple, Any

from application.exceptions import AuthenticationError, InactiveAccountError
from starlette import status
from pydantic import BaseModel, ConfigDict, Field, field_validator
from fastapi import HTTPException
from fastapi.responses import JSONResponse


class Codes(StrEnum):

    REQUEST_ERROR = "REQUEST_ERROR"
    NOT_FOUND_ERROR = "NOT_FOUND_ERROR"
    CONFLICT_ERROR = "CONFLICT_ERROR"
    UNAUTHORIZED = "UNAUTHORIZED"
    FORBIDDEN = "FORBIDDEN"
    VALIDATION_ERROR = "VALIDATION_ERROR"


class ErrorMessages(StrEnum):

    invalid_login_or_password = "Неверный логин или пароль"
    error_request = "Ошибка выполнения запроса"
    account_inactive = "Аккаунт не активен"
    validation_error = "Ошибка валидации"


class HTTPExceptionContext(BaseModel):

    code: Codes = Field(
        default=Codes.REQUEST_ERROR,
        description="Код ошибки",
        examples=[Codes.REQUEST_ERROR, Codes.VALIDATION_ERROR]
    )
    message: ErrorMessages = Field(
            default=ErrorMessages.error_request,
            description="Сообщение об ошибке",
            examples=[ErrorMessages.error_request, ErrorMessages.validation_error]
    )
    user_message: ErrorMessages = Field(
        default=ErrorMessages.error_request,
        description="Сообщение для пользователя",
        examples=[ErrorMessages.validation_error]
    )
    timestamp: str = Field(
        description="Время возникновения ошибки",
        default_factory=lambda: datetime.now().isoformat()
    )

    @cached_property
    def http_status(self) -> int:
        """Определяет HTTP статус на основе кода ошибки."""
        status_map = {
            Codes.REQUEST_ERROR: status.HTTP_500_INTERNAL_SERVER_ERROR,
            Codes.VALIDATION_ERROR: status.HTTP_422_UNPROCESSABLE_ENTITY,
            Codes.UNAUTHORIZED: status.HTTP_401_UNAUTHORIZED,
            Codes.FORBIDDEN: status.HTTP_403_FORBIDDEN,
            Codes.NOT_FOUND_ERROR: status.HTTP_404_NOT_FOUND,
            Codes.CONFLICT_ERROR: status.HTTP_409_CONFLICT,
        }
        return status_map.get(self.code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    model_config = ConfigDict(
        use_enum_values=True,
        json_schema_extra={
            "example": {
                "code": Codes.VALIDATION_ERROR,
                "message": ErrorMessages.validation_error,
                "user_message": ErrorMessages.validation_error,
                "timestamp": "2024-01-15T10:30:00.000Z",
            }
        }
    )

    def to_json_response(
        self,
        custom_status: int | None = None,
    ) -> JSONResponse:
        """
        Конвертирует Detail в JSONResponse.

        Args:
            custom_status: Кастомный HTTP статус
        Returns:
            JSONResponse
        """
        return JSONResponse(
            status_code=custom_status or self.http_status,
            content=self.model_dump(exclude_none=True),
        )

    def to_http_exception(
        self,
        custom_status: int | None = None,
        headers: dict[str, str] | None = None,
    ) -> HTTPException:
        """
        Конвертирует Detail в HTTPException.

        Args:
            custom_status: Кастомный HTTP статус (если не указан, используется http_status)
            headers: Дополнительные HTTP заголовки

        Returns:
            HTTPException с сериализованным Detail в detail
        """
        return HTTPException(
            status_code=custom_status or self.http_status,
            detail=self.model_dump(exclude_none=True),
            headers=headers,
        )

