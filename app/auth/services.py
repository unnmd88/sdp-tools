from fastapi import Form, HTTPException
from sqlalchemy import select
from starlette import status

from auth import utils as auth_utils
from auth.schemas import UserSchema
from core.models import User, db_api
from users.crud import get_user_by_username_or_none

unauthed_exc = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail='invalid username or password'
)


def check_user_is_active(user_is_active: bool) -> bool:
    if not user_is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail='inactive user'
        )
    return True


def check_password_is_valid(plain_password: str, hashed_password: bytes) -> bool:
    if not auth_utils.validate_password(
        password=plain_password, hashed_password=hashed_password
    ):
        raise unauthed_exc
    return True


async def validate_auth_user(
    username: str = Form(),
    password: str = Form(),
):
    if (user := await get_user_by_username_or_none(username)) is None:
        raise unauthed_exc
    check_password_is_valid(password, user.password)
    check_user_is_active(user.is_active)
    return UserSchema.model_validate(user, from_attributes=True)