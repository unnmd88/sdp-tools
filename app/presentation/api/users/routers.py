from fastapi import APIRouter, status, HTTPException

from core.dto.users import (
    CreateUserDTO,
    UpdateUserDTO,
    SearchUserByIdDTO,
    SearchUsersDTO
)

from core.users.exceptions import UserAlreadyExistsError, DomainValidationError, InvalidUserPasswordToSetError, \
    UserPermissionsError
from presentation.api.dependencies.deps import (
    UsersCrudUseCase,
    PayloadJWT,
    IsSuperuser
)

from presentation.schemas.users import (
    CreateUserSchema,
    ResponseUserSchema,
    UpdateUserSchema,
    ChangeUserPasswordSchema,
)

router = APIRouter(
    prefix='/users',
    tags=['Users'],
    # dependencies=[IsSuperuser],
)


@router.get(
    '/whoami/',
    status_code=status.HTTP_200_OK,
    response_model=ResponseUserSchema,
)
async def whoami(
    payload_jwt: PayloadJWT,
    use_case: UsersCrudUseCase,
):
    user_search_dto = SearchUserByIdDTO(
        customer_id=payload_jwt.user_id,
        search_user_id=payload_jwt.user_id,
    )
    user = await use_case.get_user_by_id(user_search_dto)
    return ResponseUserSchema.model_validate(user, from_attributes=True)


@router.get(
    '/',
    status_code=status.HTTP_200_OK,
    response_model=list[ResponseUserSchema],
    dependencies=[IsSuperuser],
)
async def get_users(
    payload_jwt: PayloadJWT,
    use_case: UsersCrudUseCase,
):
    user_search_dto = SearchUsersDTO(customer_id=payload_jwt.user_id)
    users = await use_case.get_all_users(user_search_dto)
    return [
        ResponseUserSchema.model_validate(user, from_attributes=True)
        for user in users
    ]


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    # response_model=ResponseUserSchema,
    # dependencies=[IsSuperuser],
)
async def create_user(
    jwt_payload: PayloadJWT,
    new_user: CreateUserSchema,
    use_case: UsersCrudUseCase,
):
    create_model_fields = new_user.model_dump(exclude_unset=True)
    create_model_fields.update(customer_id=jwt_payload.user_id)
    user_dto = CreateUserDTO(**create_model_fields)
    new_user_entity = err = _status_code = None
    try:
        new_user_entity = await use_case.create_user(user_dto)
    except DomainValidationError as e:
        err = f'Некорректные данные для создания нового пользователя: {e}.'
        _status_code = status.HTTP_422_UNPROCESSABLE_CONTENT
    except InvalidUserPasswordToSetError:
        err = 'Недопустимый пароль.'
        _status_code = status.HTTP_422_UNPROCESSABLE_CONTENT
    except UserAlreadyExistsError:
        err = 'Пользователь с данным username уже существует.'
        _status_code = status.HTTP_409_CONFLICT
    except UserPermissionsError:
        err = 'Нет прав для создания нового пользователя.'
        _status_code = status.HTTP_403_FORBIDDEN
    if err is not None:
        raise HTTPException(status_code=_status_code, detail=err)
    return new_user_entity


@router.patch(
    '/',
    status_code=status.HTTP_200_OK,
    # response_model=UserSchema,
    # dependencies=[IsSuperuser],

)
async def update_user(
    payload_jwt: PayloadJWT,
    to_update: UpdateUserSchema,
    use_case: UsersCrudUseCase,
):
    upd_user_dto = UpdateUserDTO(
        **to_update.model_dump()
        | {'requester_username': payload_jwt.sub, 'is_active': True}
    )
    return await use_case.update_user(upd_user_dto)


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
