from fastapi import APIRouter, status, Depends

from application.dto.users import ChangeUserPasswordByAdminDTO, CreateUserDTO

from presentation.api.dependencies.ioc import (
    CreateUserUseCase,
    AccessTokenDep,
    ResetPasswordUseCase,
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
    token_dto: AccessTokenDep,
    new_user: CreateUserSchema,
    use_case: CreateUserUseCase,
) -> ResponseUserSchema:
    user_dto = CreateUserDTO(
        customer_id=token_dto.user_id,
        **new_user.model_dump(),
    )
    return ResponseUserSchema.model_validate(
        await use_case(user_dto),
        from_attributes=True,
    )


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
