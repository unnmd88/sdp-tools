from typing import Annotated

from fastapi import APIRouter, status, HTTPException, Depends

from application.dto.jwt_dto import AccessJWTPayloadDTO
from application.dto.users import ChangeUserPasswordByAdminDTO
from domain.enums.unsorted import TokenTypesEnum
from presentation.api.api_v1.documentation.users.endpoints import GET_whoami
from presentation.api.dependencies.di import jwt_decoder_factory
from presentation.api.dependencies.ioc import (
    # IsSuperuser,
    # PayloadAccessJWT,
    # UsersUseCase,
    CreateUserUseCase, AccessTokenDep, ResetPasswordUseCase,
)
from presentation.schemas.users import CreateUserSchema, ResponseUserSchema, ChangeUserPasswordBaseSchema, \
 UpdatedPasswordByAdminResponse

router = APIRouter(
    prefix="/admin",
    tags=["Administration"],
)


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
    "/create-user/",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseUserSchema,
    # dependencies=[IsSuperuser],
    summary="Создать нового пользователя системы",
)
async def create_user(
    # jwt_payload: PayloadAccessJWT,
    # new_user: CreateUserSchema,
    # use_case: CreateUserUseCase,
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
        err = f"Некорректные данные для создания нового пользователя: {e}."
        _status_code = status.HTTP_422_UNPROCESSABLE_CONTENT
    except UserAlreadyExistsError:
        err = "Пользователь с данным username уже существует."
        _status_code = status.HTTP_409_CONFLICT
    except UserPermissionsError:
        err = "Нет прав для создания нового пользователя."
        _status_code = status.HTTP_403_FORBIDDEN
    if err is not None:
        raise HTTPException(status_code=_status_code, detail=err)
    return new_user_entity


@router.patch(
    "/reset-user-password/{username}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=UpdatedPasswordByAdminResponse,
)
async def change_user_password(
    username: str,
    token_dto: AccessTokenDep,
    use_case: ResetPasswordUseCase,
) -> UpdatedPasswordByAdminResponse:
    dto = ChangeUserPasswordByAdminDTO(customer_id=token_dto.user_id, subject_username=username)
    return UpdatedPasswordByAdminResponse.model_validate(
        await use_case(dto),
        from_attributes=True,
    )
