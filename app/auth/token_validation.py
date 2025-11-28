from typing import Annotated

# from core.database import db_api
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import ExpiredSignatureError, InvalidTokenError

from infrastructure.database.api import db_api
from users.crud import get_user_by_id
from users.schemas import UserFromDbFullSchema

from auth.constants import TokenFields, TokenTypes
from auth.exceptions import (
    ExpiredSignatureJWT,
    ForbiddenSelfUser,
    InactiveUserError,
    InvalidErrorJWT,
    get_invalid_type_jwt_exception,
)
from auth.utils import decode_jwt

http_bearer = HTTPBearer()


def extract_payload_from_jwt(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(http_bearer)],
) -> dict:
    try:
        payload = decode_jwt(credentials.credentials)
    except ExpiredSignatureError:
        raise ExpiredSignatureJWT
    except InvalidTokenError:
        raise InvalidErrorJWT
    return payload


async def check_user_is_active(
    payload: Annotated[dict, Depends(extract_payload_from_jwt)],
) -> UserFromDbFullSchema:
    async with db_api.session_factory() as session:
        user = await get_user_by_id(payload.get(TokenFields.user_id), session)
    if not user.is_active:
        raise InactiveUserError
    return user


async def check_is_active_superuser(
    user: Annotated[UserFromDbFullSchema, Depends(check_user_is_active)],
) -> UserFromDbFullSchema:
    if not user.is_superuser:
        raise ForbiddenSelfUser
    return user


def check_token_type(
    token_type: TokenTypes,
    expected_type: TokenTypes,
) -> bool:
    if token_type != expected_type:
        raise get_invalid_type_jwt_exception(token_type, expected_type)
    return True
