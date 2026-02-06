from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    status,
)

from application.dto.jwt_dto import AccessJWTPayloadDTO
from application.dto.users import UserDTO, ChangeUserPasswordDTO
from application.services.user_service import UserServiceImpl

from domain.enums.unsorted import TokenTypesEnum
from presentation.api.api_v1.documentation.users.endpoints import GET_whoami
from presentation.api.dependencies.di import (
    jwt_decoder_factory,
    get_user_service,
)
from presentation.api.dependencies.ioc import ChangePasswordUseCase, AccessTokenDep

from presentation.schemas.users import (
    ResponseUserSchema,
    ChangeUserPasswordBaseSchema,
)

router = APIRouter(
    prefix="/user",
    tags=["Users"],
    # dependencies=[BEARER_TOKEN],
)


@router.get(
    "/whoami/",
    status_code=status.HTTP_200_OK,
    response_model=ResponseUserSchema,
    summary="Данные о пользователе из access jwt",
    description=GET_whoami,
)
async def whoami(
    token_dto: AccessTokenDep,
    user_service: Annotated[UserServiceImpl, Depends(get_user_service)],
):
    return ResponseUserSchema.model_validate(
        obj=UserDTO.from_entity(await user_service.get_user_by_id_or_raise(token_dto.user_id)),
        from_attributes=True,
    )


# @router.patch(
#     "/",
#     status_code=status.HTTP_200_OK,
#     # response_model=UserSchema,
#     # dependencies=[IsSuperuser],
# )
# async def update_user(
#     # payload_jwt: PayloadAccessJWT,
#     # to_update: UpdateUserSchema,
#     # use_case: UsersUseCase,
# ):
#     upd_user_dto = UpdateUserDTO(
#         **to_update.model_dump()
#         | {"requester_username": payload_jwt.sub, "is_active": True}
#     )
#     return await use_case.update(upd_user_dto)


@router.patch(
    "/change-password/",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=ChangeUserPasswordBaseSchema,
)
async def change_user_password(
    token_dto: Annotated[
        AccessJWTPayloadDTO,
        Depends(jwt_decoder_factory(token_type=TokenTypesEnum.access)),
    ],
    change_password: ChangeUserPasswordBaseSchema,
    use_case: ChangePasswordUseCase,
):
    change_password_dto = ChangeUserPasswordDTO(**change_password.model_dump())
    res_change_password_dto = await use_case(user_id=token_dto.user_id, change_password_dto=change_password_dto)

    return ChangeUserPasswordBaseSchema.model_validate(
        res_change_password_dto,
        from_attributes=True
    )
