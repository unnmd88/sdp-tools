from fastapi import APIRouter, status, HTTPException

from core.dto.users import CreateUserDTO
from core.exceptions.base import UserPermissionsError
from core.users.exceptions import DomainValidationError, InvalidUserPasswordToSetError, UserAlreadyExistsError
from presentation.api.dependencies.deps import IsSuperuser, PayloadAccessJWT, UsersUseCase, CreateUserUseCase
from presentation.schemas.users import CreateUserSchema

router = APIRouter(
    prefix='/admin',
    tags=['Administration'],
)


@router.post(
    '/create-user/',
    status_code=status.HTTP_201_CREATED,
    # response_model=ResponseUserSchema,
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
    except DomainValidationError as e:
        err = f'Некорректные данные для создания нового пользователя: {e}.'
        _status_code = status.HTTP_422_UNPROCESSABLE_CONTENT
    except InvalidUserPasswordToSetError as e:
        err = e
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