from typing import Annotated

from auth.schemas import AuthSchema
from infrastructure.database.api import db_api
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
# from core.users import get_user_by_id

from core.enums.tokens import TokenFields, TokenTypes
# from auth import create_access_jwt, create_refresh_jwt
# from auth import TokenInfo, UserSchema
# from core.auth import validate_auth_user
# from auth import check_token_type, extract_payload_from_jwt
from presentation.api.dependencies import auth_form, AuthUseCase, auth_user_and_issue_access_and_refresh_jwt, AccessAndRefreshJWT

router = APIRouter(prefix='/auth', tags=['Authentication'])


db_session = Annotated[
    AsyncSession,
    Depends(db_api.session_getter),
]


@router.post(
    '/login/',
    # response_model=TokenInfo,
)
# async def auth_user_issue_jwt(user: UserSchema = Depends(validate_auth_user)):
# async def auth_user_and_issue_jwt(user: AuthSchema = Depends(auth_form)):
async def auth_user_and_issue_jwt(

    # use_case: AuthUseCase,
    jwt: AccessAndRefreshJWT,

):
    return jwt
    return jwt
    print(f'use_case: {use_case}')
    return await use_case.auth_and_issue_jwt(refresh=True)
    # return create_access_jwt(user)
    return TokenInfo(
        access_token=create_access_jwt(user),
        refresh_token=create_refresh_jwt(user),
    )


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
