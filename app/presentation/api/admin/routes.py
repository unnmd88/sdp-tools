from fastapi import APIRouter, status, HTTPException

from core.dto.users import CreateUserDTO, SearchUsersDTO
from core.exceptions.base import DomainValidationError
from core.exceptions.users import UserPermissionsError
from core.users.exceptions import (
    InvalidUsernameOrPasswordToSetError,
    UserAlreadyExistsError,
    InvalidValueToSetError,
)
from presentation.api.api_v1.documentation.users.endpoints import GET_whoami
from presentation.api.dependencies.deps import (
    IsSuperuser,
    PayloadAccessJWT,
    UsersUseCase,
    CreateUserUseCase,
)
from presentation.schemas.users import CreateUserSchema, ResponseUserSchema

router = APIRouter(
    prefix='/admin',
    tags=['Administration'],
)


@router.get(
    '/whoami/',
    dependencies=[IsSuperuser],
    status_code=status.HTTP_200_OK,
    response_model=ResponseUserSchema,
    summary='Данные о пользователе из access jwt',
    description=GET_whoami,
)
async def whoami(
    payload_jwt: PayloadAccessJWT,
    use_case: UsersUseCase,
):
    user = await use_case.get_user_by_username_or_raise(username=payload_jwt.sub)
    return ResponseUserSchema.model_validate(user, from_attributes=True)


# @router.get(
#     '/',
#     status_code=status.HTTP_200_OK,
#     response_model=list[ResponseUserSchema],
#     dependencies=[IsSuperuser],
#     summary='Получить список пользователей системы',
#
# )
# async def get_users(
#     payload_jwt: PayloadAccessJWT,
#     use_case: UsersUseCase,
# ):
#     user_search_dto = SearchUsersDTO(customer=payload_jwt.user_id)
#     try:
#         users = await use_case.get_all(user_search_dto)
#     except UserPermissionsError:
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail='Доступ к данным пользователей запрещен.'
#         )
#     return [
#         ResponseUserSchema.model_validate(user, from_attributes=True)
#         for user in users
#     ]


@router.post(
    '/create-user/',
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseUserSchema,
    dependencies=[IsSuperuser],
    summary='Создать нового пользователя системы',
)
async def create_user(
    jwt_payload: PayloadAccessJWT,
    new_user: CreateUserSchema,
    use_case: CreateUserUseCase,
):
    create_model_fields = new_user.model_dump()
    create_model_fields.update(customer=jwt_payload.sub)
    user_dto = CreateUserDTO(**create_model_fields)
    new_user_entity = err = _status_code = None
    try:
        new_user_entity = await use_case(user_dto)
    except InvalidValueToSetError as e:
        err = str(e)
        _status_code = status.HTTP_422_UNPROCESSABLE_CONTENT
    except DomainValidationError as e:
        err = f'Некорректные данные для создания нового пользователя: {e}.'
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
    '/change-user-password/{username}',
    status_code=status.HTTP_202_ACCEPTED,
    # response_model=ChangeUserPasswordResponse,
)
async def change_user_password(
    payload_jwt: PayloadAccessJWT,
    # change_password: ChangeUserPasswordBaseSchema,
    use_case: UsersUseCase,
):
    change_password_dto = ChangeUserPasswordDTO(
        customer=payload_jwt.sub,
        subject=payload_jwt.sub,
        old_password=change_password.old_password,
        new_password=change_password.new_password,
    )
    _status_code = _detail = None
    try:
        result_dto: ChangeUserPasswordDTO = await use_case.change_password(
            change_password_dto
        )
    except UserNotFoundError:
        _status_code = status.HTTP_404_NOT_FOUND
        _detail = f'Пользователь {payload_jwt.sub!r} не найден.'
    except InactiveUserError:
        _status_code = status.HTTP_403_FORBIDDEN
        _detail = f'Пользователь {payload_jwt.sub!r} не активен.'
    except UserPermissionsError:
        _status_code = status.HTTP_403_FORBIDDEN
        _detail = f'У пользователя {payload_jwt.sub!r} нет прав для изменения пароля.'
    except InvalidUsernameOrPasswordError:
        _status_code = status.HTTP_401_UNAUTHORIZED
        _detail = f'Неверный логин или пароль пользователя {payload_jwt.sub!r}.'
    except SameUsernameAndPasswordError:
        _status_code = status.HTTP_422_UNPROCESSABLE_CONTENT
        _detail = f'Пароль и логин должны отличаться.'
    except InvalidUsernameOrPasswordToSetError:
        _status_code = status.HTTP_422_UNPROCESSABLE_CONTENT
        _detail = f'Недопустимый пароль.'
    except Exception:
        # TODO Залоггировать
        _status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        _detail = f'Ошибка запроса на стороне сервера.'
    if _status_code or _detail:
        raise HTTPException(status_code=_status_code, detail=_detail)
    return ChangeUserPasswordResponse(
        subject=result_dto.subject,
        new_password=result_dto.new_password,
        old_password=result_dto.old_password,
    )
