from typing import Annotated

# from auth import (
#     # check_is_active_superuser,
#     # extract_payload_from_jwt,
# )
# from core.database import db_api
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio.session import AsyncSession

from core.users.exceptions import UserNotFoundException
from infrastructure.database.api import db_api
from core.users import crud as users_crud
from core.users.schemas import CreateUser, UserFromDbFullSchema
from infrastructure.database.user_reposirory import UsersRepositorySqlAlchemy
from presentation.api.dependencies import UsersCrudUseCase, PayloadJWTDependency
from presentation.api.exceptions import UserNotFoundHttpException

router = APIRouter(prefix='/users', tags=['Users'])


db_session = Annotated[
    AsyncSession,
    Depends(db_api.session_getter),
]
# jwt_payload = Annotated[dict, Depends(extract_payload_from_jwt)]


@router.get(
    '/whoami/',
    status_code=status.HTTP_200_OK,
    # response_model=UserFromDbFullSchema,
)
def whoami(
    # user: Annotated[UserFromDbFullSchema, Depends(check_is_active_superuser)],
    user: PayloadJWTDependency,
):
    return user


@router.get(
    '/username/{username}/',
    description='Get user by username',
    # response_model=UserFromDbFullSchema,
    # dependencies=[Depends(check_user_is_active)],
)
async def get_user_by_username(
    username: str,
    sess: db_session,
    # use_case: Annotated[UsersUseCaseProtocol, Depends(get_user)],
    use_case: UsersCrudUseCase,
):
    try:
        return await use_case.get_user_by_username_or_none(username)
    except UserNotFoundException as e:
        raise UserNotFoundHttpException(detail=e.detail)
    return await users_crud.get_user_by_id(user_id, sess)
    return await users_crud.get_user_by_id(user_id, sess)


@router.get(
    '/{user_id}/',
    description='Get user by id',
    # response_model=UserFromDbFullSchema,
    # dependencies=[Depends(check_user_is_active)],
)
async def get_user(
    user_id: int,
    sess: db_session,
    use_case: UsersCrudUseCase,
):
    try:
        return await use_case.get_user_by_id(user_id)
    except UserNotFoundException as e:
        raise UserNotFoundHttpException(detail=e.detail)
    return await use_case.user_service.find_by_id(user_id)
    return await users_crud.get_user_by_id(user_id, sess)
    return await users_crud.get_user_by_id(user_id, sess)


@router.get(
    '/',
    # response_model=list[UserFromDbFullSchema],
    # dependencies=[Depends(check_is_active_superuser)],
)
async def get_users(
    sess: db_session,
):
    repo = UsersRepositorySqlAlchemy(sess)
    return await repo.get_all()
    # return await users_crud.get_users(session=sess)


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=UserFromDbFullSchema,
    # dependencies=[Depends(check_is_active_superuser)],
)
async def create_user(
    user: CreateUser,
    sess: db_session,
) -> UserFromDbFullSchema:
    return UserFromDbFullSchema.model_validate(
        obj=await users_crud.create_user(user, sess),
        from_attributes=True,
    )
