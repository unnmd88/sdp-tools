from typing import Annotated

from fastapi import APIRouter, HTTPException
from starlette import status

from application.dto.auth import UserAuthDTO
from application.exceptions import AuthenticationError, InactiveAccountError
from presentation.api.api_v1.documentation.auth_and_jwt.endpoints import (
    POST_LOGIN_user,
    POST_REFRESH,
)
from presentation.api.dependencies.di import oauth2_scheme
from presentation.api.dependencies.ioc import (
    AuthForm,
    LoginAndIssueJWTUseCase,
    RefreshJWTUseCase,
    # RefreshJWTUseCase
)
from fastapi.params import Depends

from presentation.api.response_detail import HTTPExceptionContext, Codes, ErrorMessages
from presentation.schemas.jwt import TokenInfo

router = APIRouter(prefix="/auth", tags=["Authentication"])



AUTH_RESPONSES = {
    status.HTTP_200_OK: {
        "model": TokenInfo,
    },
    status.HTTP_401_UNAUTHORIZED: {
        "model": HTTPExceptionContext,
        "description": "Неверный логин или пароль",
        "content": {
            "application/json": {
                "example": {
                    "detail":
                        HTTPExceptionContext(
                            code=Codes.UNAUTHORIZED,
                            message=ErrorMessages.invalid_login_or_password,
                            user_message=ErrorMessages.invalid_login_or_password
                        ).model_dump()
                }
            }
        }
    },
    status.HTTP_403_FORBIDDEN: {
        "model": HTTPExceptionContext,
        "description": "Пользователь неактивен.",
        "content": {
            "application/json": {
                "example": {
                    "detail":
                        HTTPExceptionContext(
                            code=Codes.FORBIDDEN,
                            message=ErrorMessages.account_inactive,
                            user_message=ErrorMessages.account_inactive
                        ).model_dump(),
                },
            },
        },
    },
    status.HTTP_500_INTERNAL_SERVER_ERROR: {
        "model": HTTPExceptionContext,
        "description": "Внутренняя ошибка сервера",
        "content": {
            "application/json": {
                "example": {
                    "detail":
                        HTTPExceptionContext(
                            code=Codes.REQUEST_ERROR,
                            message=ErrorMessages.error_request,
                            user_message=ErrorMessages.error_request
                        ).model_dump()

                }
            }
        }
    }
}


@router.post(
    "/login/",
    # response_model=TokenInfo,
    response_model_exclude_none=True,
    summary="Аутентификация пользователя и выпуск jwt",
    description=POST_LOGIN_user,
    responses=AUTH_RESPONSES,
)
async def login_and_issue_jwt(
    auth_schema: AuthForm,
    use_case: LoginAndIssueJWTUseCase,
):
    auth_dto = UserAuthDTO(
        username=auth_schema.username,
        password=auth_schema.password,
    )
    try:
        return await use_case(auth_dto=auth_dto)
    except AuthenticationError:
        e = HTTPExceptionContext(
            code=Codes.UNAUTHORIZED,
            message=ErrorMessages.invalid_login_or_password,
            user_message=ErrorMessages.invalid_login_or_password,
        )
    except InactiveAccountError:
        e = HTTPExceptionContext(
            code=Codes.FORBIDDEN,
            message=ErrorMessages.account_inactive,
            user_message=ErrorMessages.account_inactive
        )
    except Exception:
        e = HTTPExceptionContext(
            code=Codes.REQUEST_ERROR,
            message=ErrorMessages.error_request,
            user_message=ErrorMessages.error_request
        )
    raise e.to_http_exception()




@router.post(
    "/refresh/",
    response_model=TokenInfo,
    response_model_exclude_none=True,
    summary="Выпуск access jwt по refresh jwt",
    description=POST_REFRESH,
)
async def issue_access_by_refresh_jwt(
    token: Annotated[str | bytes, Depends(oauth2_scheme)],
    use_case: RefreshJWTUseCase,
):
    try:
        return await use_case(refresh_jwt=token)
    except (UnauthorizedError, ForbiddenError, InvalidTokenTypeError) as e:
        raise HTTPException(
            detail=e.message,
            status_code=e.http_status,
        )
