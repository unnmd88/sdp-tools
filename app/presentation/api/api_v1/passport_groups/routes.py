from collections.abc import Sequence

# from core.dependencies import db_session
from fastapi import (
    APIRouter,
)
from starlette import status

from presentation.api.api_v1.passport_groups.crud import PassportGroupsCrud
from presentation.api.api_v1.passport_groups.schemas import (
    PassportGroupsCreate,
    PassportGroupsSchema,
    PassportGroupsUpdate,
)
from presentation.api.dependencies.dependencies import db_session

router = APIRouter(
    prefix='/passport-groups',
    tags=['Passport groups'],
    # dependencies=[Depends(check_user_is_active)],
)


@router.get(
    '/{id}',
    status_code=status.HTTP_200_OK,
    response_model=PassportGroupsSchema,
)
async def get_group(
    group_id: int,
    session: db_session,
) -> PassportGroupsSchema:
    owner = await PassportGroupsCrud.get_one_by_id_or_404(
        session=session, pk_id=group_id
    )
    return PassportGroupsSchema.model_validate(
        obj=owner,
        from_attributes=True,
    )


@router.get(
    '/', status_code=status.HTTP_200_OK, response_model=Sequence[PassportGroupsSchema]
)
async def get_all_groups(
    session: db_session,
) -> Sequence[PassportGroupsSchema]:
    return await PassportGroupsCrud.get_all(
        session,
    )


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
