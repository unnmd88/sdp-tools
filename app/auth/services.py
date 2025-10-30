from fastapi import Form
from users.crud import get_user_by_username_or_none

from auth import utils as auth_utils
from auth.exceptions import AuthenticationError, InactiveUserError
from auth.schemas import UserSchema


def check_user_is_active(user_is_active: bool) -> bool:
    if not user_is_active:
        raise InactiveUserError
    return True


def check_password_is_valid(plain_password: str, hashed_password: bytes) -> bool:
    if not auth_utils.validate_password(
        password=plain_password, hashed_password=hashed_password
    ):
        raise AuthenticationError
    return True


async def validate_auth_user(
    username: str = Form(),
    password: str = Form(),
):
    if (user := await get_user_by_username_or_none(username)) is None:
        raise AuthenticationError
    check_password_is_valid(password, user.password)
    check_user_is_active(user.is_active)
    return UserSchema.model_validate(user, from_attributes=True)
