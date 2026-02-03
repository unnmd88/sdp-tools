from datetime import datetime
from enum import StrEnum
from functools import cached_property
from typing import NamedTuple

from starlette import status
from pydantic import BaseModel, ConfigDict, Field, field_validator
from fastapi import HTTPException, FastAPI, Request
from fastapi.responses import JSONResponse

from application.exceptions import AuthenticationError
from core.exceptions import BaseAppError
from domain.exceptions import DomainContractViolationError, DomainEntityNotFoundError
from infrastructure.exceptions import RepositoryCorruptedError


class Codes(StrEnum):
    REQUEST_ERROR = "REQUEST_ERROR"
    BAD_REQUEST_ERROR = "REQUEST_ERROR"
    NOT_FOUND_ERROR = "NOT_FOUND_ERROR"
    CONFLICT_ERROR = "CONFLICT_ERROR"
    UNAUTHORIZED = "UNAUTHORIZED"
    FORBIDDEN = "FORBIDDEN"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR"


class CodeMapping(NamedTuple):
    code: Codes
    http_status: int


class ErrorMessages(StrEnum):
    invalid_login_or_password = "Неверный логин или пароль"
    error_request = "Ошибка выполнения запроса"
    account_inactive = "Аккаунт не активен"
    validation_error = "Ошибка валидации"
    internal_server_error = "Внутренняя ошибка сервера"


class HTTPExceptionContext(BaseModel):

    http_status: int = Field(..., description="HTTP статус", exclude=True)

    code: Codes = Field(
        default=Codes.REQUEST_ERROR,
        description="Код ошибки",
        examples=[Codes.REQUEST_ERROR, Codes.VALIDATION_ERROR],
    )
    message: str = Field(
        default=ErrorMessages.error_request,
        description="Сообщение об ошибке",
        examples=[ErrorMessages.error_request, ErrorMessages.validation_error],
    )

    model_config = ConfigDict(
        use_enum_values=True,
        json_schema_extra={
            "example": {
                "code": Codes.VALIDATION_ERROR,
                "message": ErrorMessages.validation_error,
            }
        },
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

status_map = {
    DomainContractViolationError: CodeMapping(code=Codes.BAD_REQUEST_ERROR, http_status=status.HTTP_422_UNPROCESSABLE_ENTITY),
    RepositoryCorruptedError: CodeMapping(code=Codes.INTERNAL_SERVER_ERROR, http_status=status.HTTP_500_INTERNAL_SERVER_ERROR),
    DomainEntityNotFoundError: CodeMapping(code=Codes.NOT_FOUND_ERROR, http_status=status.HTTP_404_NOT_FOUND),
    AuthenticationError: CodeMapping(code=Codes.UNAUTHORIZED, http_status=status.HTTP_401_UNAUTHORIZED),
}

def setup_exception_handlers(app: FastAPI) -> None:


    @app.exception_handler(Exception)
    async def global_exception_handler(
        request: Request,
        exc: Exception,
    ) -> JSONResponse:

        code_mapping = CodeMapping(code=Codes.REQUEST_ERROR, http_status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return HTTPExceptionContext(
            http_status=code_mapping.http_status,
            code=code_mapping.code,
            message="Серверная ошибка обработки запроса."
        ).to_json_response()



    @app.exception_handler(BaseAppError)
    async def app_exception_handler(
        request: Request,
        exc: BaseAppError,
    ) -> JSONResponse:
        c = status_map[AuthenticationError]
        print(f"{c=}")
        print(f"exc == AuthenticationError {exc == AuthenticationError}")
        code_mapping = status_map.get(exc.__class__, CodeMapping(code=Codes.REQUEST_ERROR, http_status=status.HTTP_500_INTERNAL_SERVER_ERROR))
        print(f"{code_mapping=}")
        print(f"{exc=}")
        e = HTTPExceptionContext(
            code=code_mapping.code,
            http_status=code_mapping.http_status,
            message=str(exc.public_message)
        )
        print(e)
        return HTTPExceptionContext(
            code=code_mapping.code,
            http_status=code_mapping.http_status,
            message=str(exc.public_message)
        ).to_json_response()
