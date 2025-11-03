from typing import Annotated

from core.models import db_api
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from users.crud import get_user_by_id

from auth.constants import TokenFields, TokenTypes
from auth.create_tokens import create_access_jwt, create_refresh_jwt
from auth.exceptions import InactiveUserError
from auth.schemas import TokenInfo, UserSchema
from auth.services import validate_auth_user
from auth.token_validation import check_token_type, extract_payload_from_jwt

router = APIRouter(prefix='/auth', tags=['Authentication'])


db_session = Annotated[
    AsyncSession,
    Depends(db_api.session_getter),
]


@router.post(
    '/login/',
    response_model=TokenInfo,
)
async def auth_user_issue_jwt(user: UserSchema = Depends(validate_auth_user)):
    return TokenInfo(
        access_token=create_access_jwt(user),
        refresh_token=create_refresh_jwt(user),
    )


@router.post(
    '/refresh/',
    response_model=TokenInfo,
    response_model_exclude_none=True,
)
async def auth_refresh_jwt(
    payload: Annotated[dict, Depends(extract_payload_from_jwt)], sess: db_session
):
    token_type = payload.get(TokenFields.typ)
    check_token_type(
        token_type=token_type,
        expected_type=TokenTypes.refresh,
    )
    user = await get_user_by_id(payload.get(TokenFields.user_id), sess)
    if not user.is_active:
        raise InactiveUserError
    return TokenInfo(
        access_token=create_access_jwt(user),
    )
