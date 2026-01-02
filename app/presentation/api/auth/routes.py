from fastapi import APIRouter, HTTPException
from starlette import status

from core.dto.auth import UserAuthDTO
from core.security_policies.exceptions import InvalidUsernameOrPasswordError
from core.users.exceptions import UserNotFoundByIdError
from presentation.api.dependencies.deps import (
    AuthForm,
    PayloadRefreshJWT,
    AuthAndJWTUseCase
)

from presentation.api.exceptions import InactiveUserException
from presentation.schemas.jwt import TokenInfo

router = APIRouter(prefix='/auth', tags=['Authentication'])


@router.post(
    '/login/',
    response_model=TokenInfo,
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
        return await use_case.authenticate_and_issue_jwt(auth_dto, refresh_token=True)
    except InvalidUsernameOrPasswordError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    except InactiveUserException:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)


@router.post(
    '/refresh/',
    response_model=TokenInfo,
    response_model_exclude_none=True,
)
async def issue_jwt_by_refresh_jwt(
    payload: PayloadRefreshJWT,
    use_case: AuthAndJWTUseCase,
):
    try:
        return await use_case.issue_jwt_by_user_id(payload.user_id, refresh_token=False)
    except UserNotFoundByIdError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
