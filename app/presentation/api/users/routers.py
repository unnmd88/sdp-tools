from typing import Annotated

from fastapi import APIRouter, status, HTTPException, Request
from fastapi.params import Depends

from application.use_cases.exceptions import UseCaseError
from domain.dto.users import (
    CreateUserDTO,
    UpdateUserDTO,
    GetUserFromRepoDTO,
    SearchUsersDTO,
    ChangeUserPasswordDTO,
)

from domain.enums.unsorted import Roles

from domain._exceptions.users import UserPermissionsError
from presentation.api.api_v1.documentation.users.endpoints import GET_whoami
from presentation.api.dependencies.di import oauth2_scheme
from presentation.api.dependencies.ioc import (
    UsersUseCase,
    PayloadAccessJWT,
    IsSuperuser,
    BEARER_TOKEN,
    GetActiveUserFromRepoByJWTUseCase,
)
from presentation.custom_roters.jwt_require_router import (
    JWTUserAPIRoute,
    jwt_route_class_factory,
)

from presentation.schemas.users import (
    CreateUserSchema,
    ResponseUserSchema,
    UpdateUserSchema,
    ChangeUserPasswordBaseSchema,
    ChangeUserPasswordResponse,
    ChangePasswordMyselfSchema,
)

router = APIRouter(
    prefix="/user",
    tags=["Users"],
    dependencies=[BEARER_TOKEN],
)

# require_active_user_router = APIRouter(
#     prefix="/user",
#     tags=["Users"],
#     # route_class=jwt_route_class_factory(active_user_require=True),
#     dependencies=[Depends(load_active_user_to_request_from_jwt)],
# )


@router.get(
    "/whoami/",
    status_code=status.HTTP_200_OK,
    response_model=ResponseUserSchema,
    summary="Данные о пользователе из access jwt",
    description=GET_whoami,
)
async def whoami(
    token: BEARER_TOKEN,
    use_case: GetActiveUserFromRepoByJWTUseCase,
):
    try:
        user_dto = await use_case(access_token=token)
        return ResponseUserSchema.model_validate(
            user_dto,
            from_attributes=True,
        )
    except UseCaseError as e:
        raise HTTPException(
            status_code=e.http_status,
            detail=e.message,
        )


@router.patch(
    "/",
    status_code=status.HTTP_200_OK,
    # response_model=UserSchema,
    # dependencies=[IsSuperuser],
)
async def update_user(
    payload_jwt: PayloadAccessJWT,
    to_update: UpdateUserSchema,
    use_case: UsersUseCase,
):
    upd_user_dto = UpdateUserDTO(
        **to_update.model_dump()
        | {"requester_username": payload_jwt.sub, "is_active": True}
    )
    return await use_case.update(upd_user_dto)


@router.patch(
    "/change-password/",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=ChangeUserPasswordResponse,
)
async def change_user_password(
    payload_jwt: PayloadAccessJWT,
    change_password: ChangePasswordMyselfSchema,
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
        _detail = f"Пользователь {payload_jwt.sub!r} не найден."
    except InactiveUserError:
        _status_code = status.HTTP_403_FORBIDDEN
        _detail = f"Пользователь {payload_jwt.sub!r} не активен."
    except UserPermissionsError:
        _status_code = status.HTTP_403_FORBIDDEN
        _detail = f"У пользователя {payload_jwt.sub!r} нет прав для изменения пароля."
    except InvalidUsernameOrPasswordError:
        _status_code = status.HTTP_401_UNAUTHORIZED
        _detail = f"Неверный логин или пароль пользователя {payload_jwt.sub!r}."
    except SameUsernameAndPasswordError:
        _status_code = status.HTTP_422_UNPROCESSABLE_CONTENT
        _detail = f"Пароль и логин должны отличаться."
    except InvalidUsernameOrPasswordToSetError:
        _status_code = status.HTTP_422_UNPROCESSABLE_CONTENT
        _detail = f"Недопустимый пароль."
    except Exception:
        # TODO Залоггировать
        _status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        _detail = f"Ошибка запроса на стороне сервера."
    if _status_code or _detail:
        raise HTTPException(status_code=_status_code, detail=_detail)
    return ChangeUserPasswordResponse(
        subject=result_dto.subject,
        new_password=result_dto.new_password,
    )
