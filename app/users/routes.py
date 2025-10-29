from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.testing.config import db_url

from core.models import db_api
from users import crud as users_crud
from users.schemas import CreateUser

router = APIRouter(prefix='/users', tags=['Users'])


db_session = Annotated[
    AsyncSession,
    Depends(db_api.session_getter),
]


# @router.get('/username/{username}/', description='Get user by username')
# async def get_user_by_username(
#     username: str,
#     sess: db_session,
# ):
#     return await users_crud.get_user_by_username_or_none(username, sess)


@router.get('/{user_id}/', description='Get user by id')
async def get_user(
    user_id: int,
    sess: db_session,
):
    return await users_crud.get_user_by_id(user_id, sess)


@router.get('/')
async def get_users(
    sess: db_session,
):
    return await users_crud.get_users(sess)


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_user(
    user: CreateUser,
    sess: db_session,
):
    return await users_crud.create_user(user, sess)
