from datetime import datetime
from enum import StrEnum
from functools import cached_property
from typing import NamedTuple

from starlette import status
from pydantic import BaseModel, ConfigDict, Field, field_validator
from fastapi import HTTPException, FastAPI, Request
from fastapi.responses import JSONResponse

from application.exceptions import AuthenticationError, InactiveAccountError
from core.exceptions import BaseAppError
from domain.exceptions import DomainContractViolationError, DomainEntityNotFoundError
from infrastructure.exceptions import RepositoryCorruptedError, TokenExpiredError, InvalidTokenTypeError, TokenError, \
    RepositoryUpdateError


class Codes(StrEnum):
    REQUEST_ERROR = "REQUEST_ERROR"
    DATA_UPDATE_ERROR = "DATA_UPDATE_ERROR"
    INVALID_TOKEN_TYPE_ERROR = "INVALID_TOKEN_TYPE_ERROR"
    TOKEN_ERROR = "TOKEN_ERROR"
    BAD_REQUEST_ERROR = "REQUEST_ERROR"
    NOT_FOUND_ERROR = "NOT_FOUND_ERROR"
    CONFLICT_ERROR = "CONFLICT_ERROR"
    UNAUTHORIZED = "UNAUTHORIZED"
    FORBIDDEN = "FORBIDDEN"
    INACTIVE_ACCOUNT = "INACTIVE_ACCOUNT"
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
    TokenExpiredError: CodeMapping(code=Codes.UNAUTHORIZED, http_status=status.HTTP_401_UNAUTHORIZED),
    InvalidTokenTypeError: CodeMapping(code=Codes.INVALID_TOKEN_TYPE_ERROR, http_status=status.HTTP_400_BAD_REQUEST),
    TokenError: CodeMapping(code=Codes.TOKEN_ERROR, http_status=status.HTTP_400_BAD_REQUEST),
    InactiveAccountError:CodeMapping(code=Codes.INACTIVE_ACCOUNT, http_status=status.HTTP_403_FORBIDDEN),
    RepositoryUpdateError: CodeMapping(code=Codes.DATA_UPDATE_ERROR, http_status=status.HTTP_400_BAD_REQUEST),

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
        code_mapping = status_map.get(exc.__class__, CodeMapping(code=Codes.REQUEST_ERROR, http_status=status.HTTP_500_INTERNAL_SERVER_ERROR))
        return HTTPExceptionContext(
            code=code_mapping.code,
            http_status=code_mapping.http_status,
            message=str(exc.public_message)
        ).to_json_response()
