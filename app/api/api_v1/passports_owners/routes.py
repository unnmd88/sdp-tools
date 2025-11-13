from collections.abc import Sequence

from fastapi import (
    APIRouter,
)

from starlette import status

from api.api_v1.passports_owners.crud import PassportsOwnersCrud
from api.api_v1.passports_owners.schemas import PassportOwnersSchema

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
