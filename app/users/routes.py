from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio.session import AsyncSession

from core.models import db_api
from users import crud as users_crud
from users.schemas import CreateUser

router = APIRouter(prefix='/users', tags=['Users'])


session = Annotated[
    AsyncSession,
    Depends(db_api.session_getter),
]

# @router.get("/{user_id}/")
# async def get_users(
#         user_id: int,
#         sess: session,
# ):
#     stmt = select(
#         User.id,
#         User.first_name,
#         User.last_name,
#         User.username,
#         User.email,
#         User.is_active,
#         User.is_admin,
#         User.is_superuser,
#         User.role,
#         User.phone_number,
#         User.telegram,
#         User.description,
#     ).order_by(User.id)
#     result: Result = await sess.execute(stmt)
#     users = result.mappings().all()
#     usrs = list(users)
#     print(f'{usrs=} ')
#     # for u in usrs:
#     #     print(f'{u} ')
#     #     print(f'type_u: {type(u)}')
#     return usrs


@router.get('/{user_id}/')
async def get_user(
    user_id: int,
    sess: session,
):
    return await users_crud.get_user(user_id, sess)


@router.get('/')
async def get_users(
    sess: session,
):
    return await users_crud.get_users(sess)


@router.post('/', status_code=status.HTTP_201_CREATED)
async def auth_user_issue_jwt(
    user: CreateUser,
    sess: session,
):
    return await users_crud.create_user(user, sess)
