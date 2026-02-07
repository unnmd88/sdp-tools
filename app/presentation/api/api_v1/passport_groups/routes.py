from collections.abc import Sequence

from fastapi import APIRouter

from fastapi.exceptions import HTTPException
from starlette import status

# from application.dto import (
#     CreatePassportGroupDTO,
#     UpdatePassportGroupDTO,
# )
from presentation.schemas.passport_groups import (
    PassportGroupsSchema,
    PassportGroupsCreate,
    PassportGroupsUpdate,
)


router = APIRouter(
    prefix="/passport-groups",
    tags=["Passport groups"],
    # dependencies=[Depends(check_user_is_active)],
)


@router.get(
    "/name/{name}",
    status_code=status.HTTP_200_OK,
    response_model=PassportGroupsSchema,
)
async def get_group_by_name(
    group_name: str,
    # use_case: PassportGroupsCrudUseCase,
) -> PassportGroupsSchema:
    if (region := await use_case.get_passport_group_by_name(group_name)) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Регион с именем={group_name} не найден.",
        )
    return PassportGroupsSchema.model_validate(region, from_attributes=True)


@router.get(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=PassportGroupsSchema,
)
async def get_group_by_id(
    group_id: int,
    # use_case: PassportGroupsCrudUseCase,
) -> PassportGroupsSchema:
    if (region := await use_case.get_passport_group_by_id(group_id)) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Регион с id={group_id} не найден.",
        )
    return PassportGroupsSchema.model_validate(region, from_attributes=True)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=Sequence[PassportGroupsSchema],
)
async def get_all_groups(
    # use_case: PassportGroupsCrudUseCase,
) -> Sequence[PassportGroupsSchema]:
    return [
        PassportGroupsSchema.model_validate(m, from_attributes=True)
        for m in await use_case.get_all_passport_groups()
    ]


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=PassportGroupsSchema,
)
async def create_group(
    # use_case: PassportGroupsCrudUseCase,
    group_data: PassportGroupsCreate,
) -> PassportGroupsSchema:
    dto = CreatePassportGroupDTO(**group_data.model_dump())
    new_passport_group: PassportGroupEntity = await use_case.create_passport_group(dto)
    return PassportGroupsSchema.model_validate(new_passport_group, from_attributes=True)


@router.patch(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=PassportGroupsSchema,
)
async def update_group(
    # use_case: PassportGroupsCrudUseCase,
    group_data_to_update: PassportGroupsUpdate,
) -> PassportGroupsSchema:
    dto = UpdatePassportGroupDTO(**group_data_to_update.model_dump())
    updated_passport_group: PassportGroupEntity = await use_case.update_passport_group(
        dto
    )
    return PassportGroupsSchema.model_validate(
        updated_passport_group, from_attributes=True
    )
