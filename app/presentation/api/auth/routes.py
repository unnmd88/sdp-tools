from typing import Annotated

from fastapi import APIRouter, HTTPException
from starlette import status

from core.dto.auth import UserAuthDTO
from core.users.exceptions import UserNotFoundByIdError, InvalidUsernameOrPasswordError
from presentation.api.api_v1.documentation.auth_and_jwt.endpoints import (
    POST_LOGIN_user,
    POST_REFRESH,
)
from presentation.api.dependencies.deps import (
    AuthForm,
    PayloadRefreshJWT,
    AuthAndJWTUseCase,
    RefreshJWTUseCase,
    # RefreshJWTUseCase
)

from presentation.api.exceptions import InactiveUserException
from presentation.schemas.jwt import TokenInfo

router = APIRouter(prefix='/auth', tags=['Authentication'])


@router.post(
    '/login/',
    response_model=TokenInfo,
    response_model_exclude_none=True,
    summary='Аутентификация пользователя и выпуск jwt',
    description=POST_LOGIN_user,
)
async def issue_jwt(
    auth_schema: AuthForm,
    use_case: AuthAndJWTUseCase,
):
    auth_dto = UserAuthDTO(
        username=auth_schema.username,
        password=auth_schema.password,
    )
    try:
        # return await use_case.authenticate_and_issue_jwt(auth_dto, refresh_token=True)
        return await use_case(login_dto=auth_dto)
    except InvalidUsernameOrPasswordError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Неверный логин или пароль.',
        )
    except InactiveUserException:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)


@router.post(
    '/refresh/',
    response_model=TokenInfo,
    response_model_exclude_none=True,
    summary='Выпуск access jwt по refresh jwt',
    description=POST_REFRESH,
)
async def issue_jwt_by_refresh_jwt(
    payload: PayloadRefreshJWT,
    use_case: RefreshJWTUseCase,
):
    try:
        return await use_case(
            username=payload.sub,
            refresh_token=False,
        )
    except UserNotFoundByIdError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
