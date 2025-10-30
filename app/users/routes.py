from typing import Annotated

from auth.token_validation import (
    check_is_active_superuser,
    check_user_is_active,
    extract_payload_from_jwt,
)
from core.models import db_api
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio.session import AsyncSession

from users import crud as users_crud
from users.schemas import CreateUser

router = APIRouter(prefix='/users', tags=['Users'])


db_session = Annotated[
    AsyncSession,
    Depends(db_api.session_getter),
]
jwt_payload = Annotated[dict, Depends(extract_payload_from_jwt)]


@router.get(
    '/{user_id}/',
    description='Get user by id',
    dependencies=[Depends(check_user_is_active)],
)
async def get_user(
    user_id: int,
    sess: db_session,
    payload: jwt_payload,
):
    return await users_crud.get_user_by_id(user_id, sess)


@router.get('/', dependencies=[Depends(check_is_active_superuser)])
async def get_users(
    sess: db_session,
    # payload: jwt_payload,
    # payload: Annotated[dict, Depends(check_user_is_active)],
):
    # print(f'PAYLOAD: {payload}')
    return await users_crud.get_users(sess)
    return await users_crud.get_users(sess)


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(check_is_active_superuser)],
)
async def create_user(
    user: CreateUser,
    sess: db_session,
):
    return await users_crud.create_user(user, sess)
