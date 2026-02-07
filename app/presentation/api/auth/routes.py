from typing import Annotated

from fastapi import APIRouter
from starlette import status

from application.dto.auth import UserAuthDTO
from application.dto.jwt_dto import RefreshJWTPayloadDTO
from application.use_cases.users.refresh_jwt_use_case import RefreshJWTUseCaseImpl
from application.use_cases.users.user_login_and_issue_jwt_use_case import (
    UserLoginAndIssueJWTUseCaseImpl,
)
from domain.enums.unsorted import TokenTypesEnum
from presentation.api.api_v1.documentation.auth_and_jwt.endpoints import (
    POST_LOGIN_user,
    POST_REFRESH,
)
# from presentation.api.dependencies.di import oauth2_scheme, jwt_decoder_factory
# from presentation.api.dependencies.ioc import (
#     LoginAndIssueJWTUseCase,
#     RefreshJWTUseCase,
# )


from presentation.api.error_handling import HTTPExceptionContext, Codes, ErrorMessages
from presentation.api.fastapi_dependencies import AuthFormDep, RefreshTokenDep
from presentation.schemas.jwt import TokenInfo
from dishka.integrations.fastapi import FromDishka, inject


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
@inject
async def login_and_issue_jwt(
    auth_schema: AuthFormDep,
    use_case: FromDishka[UserLoginAndIssueJWTUseCaseImpl],
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
@inject
async def issue_access_by_refresh_jwt(
    token_dto: RefreshTokenDep,
    use_case: FromDishka[RefreshJWTUseCaseImpl],
):
    return TokenInfo.model_validate(
        await use_case(user_id=token_dto.user_id),
        from_attributes=True
    )

