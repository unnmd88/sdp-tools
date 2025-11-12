
from fastapi import (
    APIRouter,
)

from starlette import status

from api.api_v1.passports.crud import PassportsCrud
from api.api_v1.passports.filters import OvimPassportsFilter
from api.api_v1.passports.schemas import SavePassport, CapturePassport, SavedPassportSchema

from core.dependencies import db_session

router = APIRouter(
    prefix='/passports',
    tags=['Passports of Traffic Light Objects'],
    # dependencies=[Depends(check_user_is_active)],
)


@router.get(
    '/{owner_id}',
    status_code=status.HTTP_200_OK,
)
async def get_all_passports(
    session:  db_session,
    owner_id: int,
):
    return await PassportsCrud.get_all(
        session,
        filters=OvimPassportsFilter(owner_id=owner_id),
    )


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
)
async def capture_editing_passport_ovim(
    session:  db_session,
    passport: CapturePassport,
):
    return await PassportsCrud.capture_passport(session, passport)


@router.patch(
    '/',
    status_code=status.HTTP_202_ACCEPTED,
    response_model=SavedPassportSchema,
)
async def save_passport_ovim(
    session:  db_session,
    passport: SavePassport,
) -> SavedPassportSchema:
    res = await PassportsCrud.save_passport(session, passport)
    return SavedPassportSchema.model_validate(res, from_attributes=True)
