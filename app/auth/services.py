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


async def validate_auth_user(
    username: str = Form(),
    password: str = Form(),
):
    async with db_api.session_factory() as session:
        if (user := await get_user_by_username_or_none(username, session)) is None:
            raise unauthed_exc

    print(f'db_pass: {user.password}')
    print(f'plain_pass: {password}')

    if not auth_utils.validate_password(
        password=password, hashed_password=user.password
    ):
        raise unauthed_exc
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail='inactive user'
        )
    return UserSchema.model_validate(user, from_attributes=True)