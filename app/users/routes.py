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
from users.schemas import CreateUser, UserFromDbFullSchema

router = APIRouter(prefix='/users', tags=['Users'])


db_session = Annotated[
    AsyncSession,
    Depends(db_api.session_getter),
]
jwt_payload = Annotated[dict, Depends(extract_payload_from_jwt)]


@router.get(
    "/whoami/",
    status_code=status.HTTP_200_OK,
    response_model=UserFromDbFullSchema,
)
def whoami(
    user: Annotated[UserFromDbFullSchema, Depends(check_is_active_superuser)],
):
    return user


@router.get(
    '/{user_id}/',
    description='Get user by id',
    response_model=UserFromDbFullSchema,
    dependencies=[Depends(check_user_is_active)],
)
async def get_all_user(
    user_id: int,
    sess: db_session,
):
    return await users_crud.get_user_by_id(user_id, sess)


@router.get(
'/',
    response_model=list[UserFromDbFullSchema],
    dependencies=[Depends(check_is_active_superuser)]
)
async def get_users(
    sess: db_session,
):
    return await users_crud.get_users(sess)


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=UserFromDbFullSchema,
    dependencies=[Depends(check_is_active_superuser)],
)
async def create_user(
    user: CreateUser,
    sess: db_session,
):
    return await users_crud.create_user(user, sess)


