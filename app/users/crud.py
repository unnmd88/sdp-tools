import logging

import sqlalchemy
from app_logging.dev.config import USERS_LOGGER
from auth import utils as auth_utils
from core.models import User, db_api
from fastapi import HTTPException
from sqlalchemy.engine.result import Result
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.sql.expression import select
from starlette import status

from users.schemas import CreateUser, UserFromDbFullSchema

logger = logging.getLogger(USERS_LOGGER)


async def get_user_by_username_or_none(
    username: str,
) -> User | None:
    stmt = select(User).where(User.username == username)
    try:
        async with db_api.session_factory() as session:
            result: Result = await session.execute(stmt)
        return result.scalars().one()
    except sqlalchemy.exc.NoResultFound:
        pass
    return None


async def get_user_by_id(
    user_id: int,
    session: AsyncSession,
):
    if (res := await session.get(User, user_id)) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User with id={user_id} not found',
        )
    return UserFromDbFullSchema.model_validate(res)


async def get_users(
    session: AsyncSession,
):
    stmt = select(User).order_by(User.id)
    result: Result = await session.execute(stmt)
    return [UserFromDbFullSchema.model_validate(res) for res in result.scalars().all()]


async def create_user(user: CreateUser, sess, from_app=False):
    if user.username == 'root' and from_app is False:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='username "root" is not allowed',
        )

    user.password = auth_utils.hash_password(user.password)
    new_user = User(**user.model_dump())
    sess.add(new_user)
    try:
        await sess.commit()
        await sess.refresh(new_user)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f'User with that username already exists: {user.username!r}',
        )
    # logger.debug('Created user: %r', user)
    logger.info('Created user: %r', user)
    return user.model_dump(exclude={'password'})
