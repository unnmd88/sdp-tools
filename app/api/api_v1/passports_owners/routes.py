from collections.abc import Sequence

from fastapi import (
    APIRouter,
)

from starlette import status

from api.api_v1.passports_owners.crud import PassportsOwnersCrud
from api.api_v1.passports_owners.schemas import (
    PassportOwnersSchema,
    PassportOwnersCreate,
    PassportOwnersPatch,
)

from core.dependencies import db_session


router = APIRouter(
    prefix='/passports-owners',
    tags=['Passports owners'],
    # dependencies=[Depends(check_user_is_active)],
)


@router.get(
    '/{id}',
    status_code=status.HTTP_200_OK,
    response_model=PassportOwnersSchema,
)
async def get_owner(
    owner_id: int,
    session: db_session,
) -> PassportOwnersSchema:
    owner = await PassportsOwnersCrud.get_one_by_id_or_404(
        session=session, pk_id=owner_id
    )
    return PassportOwnersSchema.model_validate(
        obj=owner,
        from_attributes=True,
    )


@router.get(
    '/', status_code=status.HTTP_200_OK, response_model=Sequence[PassportOwnersSchema]
)
async def get_all_owners(
    session: db_session,
) -> Sequence[PassportOwnersSchema]:
    return await PassportsOwnersCrud.get_all(
        session,
    )


@router.post(
    '/',
    status_code=status.HTTP_200_OK,
    response_model=PassportOwnersSchema,
)
async def create_owner(
    session: db_session,
    owner: PassportOwnersCreate,
) -> PassportOwnersSchema:
    return await PassportsOwnersCrud.add(session=session, model=owner)


@router.patch(
    '/{id}',
    status_code=status.HTTP_200_OK,
    response_model=PassportOwnersSchema,
)
async def create_owner(
    owner_id: int,
    owner: PassportOwnersPatch,
    session: db_session,
) -> PassportOwnersSchema:
    db_model_owner = await PassportsOwnersCrud.get_one_by_id_or_404(
        session=session,
        pk_id=owner_id,
    )
    return await PassportsOwnersCrud.update(
        session=session,
        db_model=db_model_owner,
        to_update_model=owner,
    )
