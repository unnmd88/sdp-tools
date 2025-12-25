from collections.abc import Sequence

from fastapi import (
    APIRouter,
)
from fastapi.exceptions import HTTPException
from starlette import status

# from presentation.api.api_v1.passport_groups.crud import PassportGroupsCrud
from presentation.api.dependencies.dependencies import db_session
from presentation.api.dependencies.deps import PassportGroupsCrudUseCase
from presentation.schemas.passport_groups import PassportGroupsSchema, PassportGroupsCreate, PassportGroupsUpdate

router = APIRouter(
    prefix='/passport-groups',
    tags=['Passport groups'],
    # dependencies=[Depends(check_user_is_active)],
)


@router.get(
    '/name/{name}',
    status_code=status.HTTP_200_OK,
    response_model=PassportGroupsSchema,
)
async def get_group_by_name(
    group_name: str,
    use_case: PassportGroupsCrudUseCase,
) -> PassportGroupsSchema:
    if (region := await use_case.get_passport_group_by_name(group_name)) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Регион с именем={group_name} не найден.'
        )
    return PassportGroupsSchema.model_validate(region, from_attributes=True)



@router.get(
    '/{id}',
    status_code=status.HTTP_200_OK,
    response_model=PassportGroupsSchema,
)
async def get_group(
    group_id: int,
    use_case: PassportGroupsCrudUseCase,
) -> PassportGroupsSchema:
    if (region := await use_case.get_passport_group_by_id(group_id)) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Регион с id={group_id} не найден.'
        )
    return PassportGroupsSchema.model_validate(region, from_attributes=True)


@router.get(
    '/',
    status_code=status.HTTP_200_OK,
    response_model=Sequence[PassportGroupsSchema],
)
async def get_all_groups(
    use_case: PassportGroupsCrudUseCase,
) -> Sequence[PassportGroupsSchema]:
    return [
        PassportGroupsSchema.model_validate(m, from_attributes=True)
        for m in await use_case.get_all_passport_groups()
    ]


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=PassportGroupsSchema,
)
async def create_group(
    session: db_session,
    group: PassportGroupsCreate,
) -> PassportGroupsSchema:
    return await PassportGroupsCrud.add(session=session, model=group)


@router.patch(
    '/{id}',
    status_code=status.HTTP_200_OK,
    response_model=PassportGroupsSchema,
)
async def update_group(
    group_id: int,
    group_data: PassportGroupsUpdate,
    session: db_session,
) -> PassportGroupsSchema:
    db_model_owner = await PassportGroupsCrud.get_one_by_id_or_404(
        session=session,
        pk_id=group_id,
    )
    return await PassportGroupsCrud.update(
        session=session,
        db_model=db_model_owner,
        to_update_model=group_data,
    )
