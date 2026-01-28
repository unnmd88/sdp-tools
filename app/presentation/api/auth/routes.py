from typing import Annotated

from fastapi import APIRouter, HTTPException
from starlette import status

from application.dto.auth import UserAuthDTO
from application.exceptions import AuthenticationError
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

from presentation.schemas.jwt import TokenInfo

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/login/",
    response_model=TokenInfo,
    response_model_exclude_none=True,
    summary="Аутентификация пользователя и выпуск jwt",
    description=POST_LOGIN_user,
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
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный логин или пароль.",
        )



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
