from auth import utils as auth_utils
from core.models import User
from fastapi import HTTPException
from sqlalchemy.engine.result import Result
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.sql.expression import select, text
from starlette import status

from users.schemas import CreateUser


async def get_user(
    user_id: int,
    session: AsyncSession,
):
    return await session.get(User, user_id)


async def get_users(
    session: AsyncSession,
):
    stmt = select(
        User.id,
        User.first_name,
        User.last_name,
        User.username,
        User.email,
        User.is_active,
        User.is_admin,
        User.is_superuser,
        User.role,
        User.phone_number,
        User.telegram,
        User.description,
    ).order_by(User.id)
    result: Result = await session.execute(stmt)
    users = result.mappings().all()
    usrs = list(users)
    print(f'{usrs=} ')
    # for u in usrs:
    #     print(f'{u} ')
    #     print(f'type_u: {type(u)}')
    return usrs


async def create_user(user: CreateUser, sess):
    res = await sess.execute(text('SELECT * FROM users'))
    print(res)

    user.password = auth_utils.hash_password(user.password)
    new_user = User(**user.model_dump())
    sess.add(new_user)
    try:
        await sess.commit()
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f'user with that username already exists: {user.username!r}',
        )

    res = await sess.execute(text('SELECT * FROM users'))
    print(res)
    return user
