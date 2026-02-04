from typing import Annotated

from fastapi import APIRouter, HTTPException
from starlette import status

from application.dto.auth import UserAuthDTO
from application.dto.jwt_dto import RefreshJWTPayloadDTO
from application.exceptions import AuthenticationError, InactiveAccountError
from domain.enums.unsorted import TokenTypesEnum
from presentation.api.api_v1.documentation.auth_and_jwt.endpoints import (
    POST_LOGIN_user,
    POST_REFRESH,
)
from presentation.api.dependencies.di import oauth2_scheme, jwt_decoder_factory
from presentation.api.dependencies.ioc import (
    AuthForm,
    LoginAndIssueJWTUseCase,
    RefreshJWTUseCase,
)
from fastapi.params import Depends

from presentation.api.error_handling import HTTPExceptionContext, Codes, ErrorMessages
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
                "example": HTTPExceptionContext(
                        http_status=status.HTTP_401_UNAUTHORIZED,
                        code=Codes.UNAUTHORIZED,
                        message=ErrorMessages.invalid_login_or_password,
                    ).model_dump()
            }
        },
    },
    status.HTTP_403_FORBIDDEN: {
        "model": HTTPExceptionContext,
        "description": "Пользователь неактивен.",
        "content": {
            "application/json": {
                "example": HTTPExceptionContext(
                        http_status=status.HTTP_403_FORBIDDEN,
                        code=Codes.FORBIDDEN,
                        message=ErrorMessages.account_inactive,
                    ).model_dump(),
            },
        },
    },
}


@router.post(
    "/login/",
    response_model=TokenInfo,
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
    issued_jwt = await use_case(auth_dto=auth_dto)
    return TokenInfo.model_validate(issued_jwt, from_attributes=True)

@router.post(
    "/refresh/",
    response_model=TokenInfo,
    response_model_exclude_none=True,
    summary="Выпуск access jwt по refresh jwt",
    description=POST_REFRESH,
)
async def issue_access_by_refresh_jwt(
    token_dto: Annotated[
        RefreshJWTPayloadDTO,
        Depends(jwt_decoder_factory(token_type=TokenTypesEnum.refresh)),
    ],
    use_case: RefreshJWTUseCase,
):
    return await use_case(user_id=token_dto.user_id)
