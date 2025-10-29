import logging

from app_logging.dev.config import USERS_LOGGER
from auth import utils as auth_utils
from core.config import BASE_DIR
from core.models import User
from fastapi import HTTPException
from sqlalchemy.engine.result import Result
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.sql.expression import select, text
from starlette import status

from users.schemas import CreateUser, UserFromDbFullSchema

logger = logging.getLogger(USERS_LOGGER)
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)
# console_handler = logging.StreamHandler()
# file_handler = logging.FileHandler(BASE_DIR / 'users/logs/users.log')
# formatter = logging.Formatter('%(levelname)s %(message)s %(asctime)s %(name)s %(lineno)s')
# console_handler.setFormatter(formatter)
# file_handler.setFormatter(formatter)
# logger.addHandler(console_handler)
# logger.addHandler(file_handler)

# logging.basicConfig(
#     level=logging.DEBUG,
#     datefmt='%Y-%m-%d %H:%M:%S',
#     format='%(levelname)s %(message)s %(asctime)s %(name)s %(lineno)s',
#     handlers=[console_handler, file_handler],
# )


async def get_user(
    user_id: int,
    session: AsyncSession,
):
    if (res := await session.get(User, user_id)) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found",
        )
    # res = await session.get(User, user_id)
    # print(f'res: {res}')
    return UserFromDbFullSchema.model_validate(res)


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
    return list(users)


async def create_user(user: CreateUser, sess, from_app=False):

    if user.username == 'root' and from_app is False:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f'username "root" is not allowed',
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

