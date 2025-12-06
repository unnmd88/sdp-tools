from typing import Annotated
from application.dtos.auth import UserAuthDTO
from auth.exceptions import InvalidUsernameOrPasswordException, InactiveUserException
from fastapi import APIRouter, Depends

from presentation.api.dependencies.deps import JWTAuthUseCase, AuthForm

from presentation.api.exceptions import (
    UnauthorizedErrorHttp401,
    InactiveUserErrorHttp403,
)
from presentation.schemas.auth import AuthSchema
from presentation.schemas.jwt import TokenInfo

router = APIRouter(prefix='/auth', tags=['Authentication'])


@router.post(
    '/login/',
    response_model=TokenInfo,
)
async def auth_user_and_issue_jwt(
    auth_schema: AuthForm,
    use_case: JWTAuthUseCase,
):
    auth_dto = UserAuthDTO(
        username=auth_schema.username,
        password=auth_schema.password,
    )
    try:
        return await use_case.auth_and_issue_jwt(auth_dto, refresh_token=True)
    except InvalidUsernameOrPasswordException:
        raise UnauthorizedErrorHttp401
    except InactiveUserException:
        raise InactiveUserErrorHttp403


# @router.post(
#     '/refresh/',
#     response_model=TokenInfo,
#     response_model_exclude_none=True,
# )
# async def auth_refresh_jwt(
#     payload: Annotated[dict, Depends(extract_payload_from_jwt)], sess: db_session
# ):
#     token_type = payload.get(TokenFields.typ)
#     check_token_type(
#         token_type=token_type,
#         expected_type=TokenTypes.refresh,
#     )
#     user = await get_user_by_id(payload.get(TokenFields.user_id), sess)
#     if not user.is_active:
#         raise InactiveUserError
#     return TokenInfo(
#         access_token=create_access_jwt(user),
#     )


# --- Backup ----


# @router.post(
#     '/login/',
#     # response_model=TokenInfo,
# )
# # async def auth_user_issue_jwt(user: UserSchema = Depends(validate_auth_user)):
# # async def auth_user_issue_jwt(user: UserSchema = Depends(auth_form)):
# async def auth_user_issue_jwt(user: int = 1):
#     return user
#     # return create_access_jwt(user)
#     return TokenInfo(
#         access_token=create_access_jwt(user),
#         refresh_token=create_refresh_jwt(user),
#     )
#
#
# @router.post(
#     '/refresh/',
#     response_model=TokenInfo,
#     response_model_exclude_none=True,
# )
# async def auth_refresh_jwt(
#     payload: Annotated[dict, Depends(extract_payload_from_jwt)], sess: db_session
# ):
#     token_type = payload.get(TokenFields.typ)
#     check_token_type(
#         token_type=token_type,
#         expected_type=TokenTypes.refresh,
#     )
#     user = await get_user_by_id(payload.get(TokenFields.user_id), sess)
#     if not user.is_active:
#         raise InactiveUserError
#     return TokenInfo(
#         access_token=create_access_jwt(user),
#     )
