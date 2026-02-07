from collections.abc import Sequence

from fastapi import APIRouter

from fastapi.exceptions import HTTPException
from starlette import status

from application.use_cases.passport_groups.create_passport_group_use_case import CreatePassportGroupUseCaseImpl
from application.use_cases.passport_groups.read_passport_group_use_case import ReadPassportGroupUseCaseImpl
from domain.cqrs.passport_groups_commands import CreatePassportGroupCommand
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
    "/name/{name}",
    status_code=status.HTTP_200_OK,
    response_model=PassportGroupResponse,
)
@inject
async def get_group_by_name(
    group_name: str,
    read_passport_group_use_case: FromDishka[ReadPassportGroupUseCaseImpl],
) -> PassportGroupResponse:
    return PassportGroupResponse.model_validate(
        await read_passport_group_use_case.by_name(group_name),
        from_attributes=True
    )


@router.get(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=PassportGroupResponse,
)
async def get_group_by_id(
    group_id: int,
    # use_case: PassportGroupsCrudUseCase,
) -> PassportGroupResponse:
    if (region := await use_case.get_passport_group_by_id(group_id)) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Регион с id={group_id} не найден.",
        )
    return PassportGroupResponse.model_validate(region, from_attributes=True)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=Sequence[PassportGroupResponse],
)
async def get_all_groups(
    # use_case: PassportGroupsCrudUseCase,
) -> Sequence[PassportGroupResponse]:
    return [
        PassportGroupResponse.model_validate(m, from_attributes=True)
        for m in await use_case.get_all_passport_groups()
    ]


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=PassportGroupResponse,
)
@inject
async def create_passport_group(
    token_dto: AccessTokenDep,
    create_passport_group_use_case: FromDishka[CreatePassportGroupUseCaseImpl],
    new_passport_group_schema: PassportGroupsCreate,
) -> PassportGroupResponse:
    command = CreatePassportGroupCommand(
        customer_id=token_dto.user_id,
        **new_passport_group_schema.model_dump()
    )
    return PassportGroupResponse.model_validate(
        await create_passport_group_use_case(command),
        from_attributes=True,
    )

    return PassportGroupResponse.model_validate(new_passport_group, from_attributes=True)


@router.patch(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=PassportGroupResponse,
)
async def update_group(
    # use_case: PassportGroupsCrudUseCase,
    group_data_to_update: PassportGroupsUpdate,
) -> PassportGroupResponse:
    dto = UpdatePassportGroupDTO(**group_data_to_update.model_dump())
    updated_passport_group: PassportGroupEntity = await use_case.update_passport_group(
        dto
    )
    return PassportGroupResponse.model_validate(
        updated_passport_group, from_attributes=True
    )
