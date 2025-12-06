from collections.abc import Sequence

from fastapi import APIRouter, status, HTTPException


from application.dtos.users import CreateUserDTO
from application.interfaces.services import users_crud

from core.users.exceptions import UserNotFoundException, UserAlreadyExistsException
from presentation.api.dependencies.deps import UsersCrudUseCase
from presentation.api.dependencies.dependencies import PayloadJWTDependency


from presentation.api.exceptions import UserNotFoundHttpException
from presentation.schemas.users import (
    CreateUserSchema,
    ResponseUserSchema,
    UpdateUserSchema,
    ChangeUserPasswordSchema,
)

router = APIRouter(prefix='/users', tags=['Users'])


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
    response_model=ResponseUserSchema,
    # dependencies=[Depends(check_user_is_active)],
)
async def get_user(
    user_id: int,
    use_case: UsersCrudUseCase,
):
    try:
        user_entity = await use_case.get_user_by_id(user_id)
        return ResponseUserSchema.model_validate(user_entity, from_attributes=True)
    except UserNotFoundException as e:
        raise UserNotFoundHttpException(detail=e.detail)


@router.get(
    '/',
    # response_model=Sequence[ResponseUserSchema],
    # dependencies=[Depends(check_is_active_superuser)],
)
async def get_users(
    jwt_payload: PayloadJWTDependency,
    user_use_case: UsersCrudUseCase,
    use_case: UsersCrudUseCase,
):
    return await user_use_case.get_user_by_id(jwt_payload.user_id)
    return jwt_payload
    return [
        ResponseUserSchema.model_validate(user_entity, from_attributes=True)
        for user_entity in await use_case.get_all_users()
    ]


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseUserSchema,
    # dependencies=[Depends(check_is_active_superuser)],
)
async def create_user(
    jwt_payload: PayloadJWTDependency,
    user: CreateUserSchema,
    use_case: UsersCrudUseCase,
):
    user_dto = CreateUserDTO(
        **(user.model_dump() | {'requester_username': jwt_payload.sub})
    )
    try:
        new_user = await use_case.create_user(user_dto)
    except UserAlreadyExistsException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.detail,
        )
    return ResponseUserSchema.model_validate(new_user, from_attributes=True)


@router.patch(
    '/',
    status_code=status.HTTP_200_OK,
    # response_model=UserSchema,
    # dependencies=[Depends(check_is_active_superuser)],
)
async def update_user(
    to_update: UpdateUserSchema,
    use_case: UsersCrudUseCase,
): ...


@router.patch(
    '/change_password/',
    status_code=status.HTTP_200_OK,
    # response_model=UserSchema,
    # dependencies=[Depends(check_is_active_superuser)],
)
async def change_user_password(
    to_change_password: ChangeUserPasswordSchema,
    use_case: UsersCrudUseCase,
):
    user_dto = CreateUserDTO(**user.model_dump())
    return await use_case.create_user(user_dto)
