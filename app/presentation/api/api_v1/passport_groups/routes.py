from collections.abc import Sequence

from fastapi import APIRouter

from starlette import status

from application.use_cases.passport_groups.passport_group_read_use_case import (
    PassportGroupReadByNameUseCase,
)
from application.use_cases.passport_groups.types import (
    PassportGroupReadUseCase,
    PassportGroupCreateUseCase,
    PassportGroupUpdateUseCase,
    PassportGroupDeleteUseCase,
)
from domain.pssport_groups.passport_groups_commands import (
    CreatePassportGroupCommand,
    UpdatePassportGroupCommand,
    DeletePassportGroupCommand,
)
from presentation.api.fastapi_dependencies import AccessTokenDep
from presentation.schemas.passport_groups import (
    PassportGroupResponse,
    PassportGroupsCreate,
    PassportGroupsUpdate,
)
from dishka.integrations.fastapi import FromDishka, inject


router = APIRouter(
    prefix="/passport-groups",
    tags=["Passport groups"],
    # dependencies=[Depends(check_user_is_active)],
)


@router.get(
    "/{name}",
    status_code=status.HTTP_200_OK,
    response_model=PassportGroupResponse,
)
@inject
async def get_group_by_name(
    group_name: str,
    read_passport_group_use_case: FromDishka[PassportGroupReadByNameUseCase],
) -> PassportGroupResponse:
    return PassportGroupResponse.model_validate(
        await read_passport_group_use_case(group_name), from_attributes=True
    )


# @router.get(
#     "/{id}",
#     status_code=status.HTTP_200_OK,
#     response_model=PassportGroupResponse,
# )
# async def get_group_by_id(
#     group_id: int,
#     # use_case: PassportGroupsCrudUseCase,
# ) -> PassportGroupResponse:
#     if (region := await use_case.get_passport_group_by_id(group_id)) is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Регион с id={group_id} не найден.",
#         )
#     return PassportGroupResponse.model_validate(region, from_attributes=True)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=Sequence[PassportGroupResponse],
)
@inject
async def get_all_groups(
    read_passport_group_use_case: FromDishka[PassportGroupReadUseCase],
) -> Sequence[PassportGroupResponse]:
    return [
        PassportGroupResponse.model_validate(r, from_attributes=True)
        for r in await read_passport_group_use_case.get_many()
    ]


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=PassportGroupResponse,
)
@inject
async def create_passport_group(
    token_dto: AccessTokenDep,
    create_passport_group_use_case: FromDishka[PassportGroupCreateUseCase],
    new_passport_group_schema: PassportGroupsCreate,
) -> PassportGroupResponse:
    command = CreatePassportGroupCommand(
        customer_id=token_dto.user_id, **new_passport_group_schema.model_dump()
    )
    return PassportGroupResponse.model_validate(
        await create_passport_group_use_case(command),
        from_attributes=True,
    )


@router.patch(
    "/{name}",
    status_code=status.HTTP_200_OK,
    response_model=PassportGroupResponse,
)
@inject
async def update_group(
    name: str,
    token_dto: AccessTokenDep,
    update_data: PassportGroupsUpdate,
    use_case: FromDishka[PassportGroupUpdateUseCase],
) -> PassportGroupResponse:
    command = UpdatePassportGroupCommand(
        customer_id=token_dto.user_id,
        name=name,
        **update_data.model_dump(exclude_unset=True),
    )
    return PassportGroupResponse.model_validate(
        await use_case(command),
        from_attributes=True,
    )


@router.delete(
    "/{name}",
    status_code=status.HTTP_200_OK,
    response_model=PassportGroupResponse,
)
@inject
async def update_group(
    name: str,
    token_dto: AccessTokenDep,
    use_case: FromDishka[PassportGroupDeleteUseCase],
) -> PassportGroupResponse:
    command = DeletePassportGroupCommand(
        customer_id=token_dto.user_id,
        name=name,
    )
    return PassportGroupResponse.model_validate(
        await use_case(command),
        from_attributes=True,
    )
