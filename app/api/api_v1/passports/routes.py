
from fastapi import (
    APIRouter,
)

from starlette import status

from api.api_v1.passports.crud import OvimPassportsCrud
from api.api_v1.passports.schemas import SavePassport, CapturePassport, SavedPassportSchema

from core.dependencies import db_session

router = APIRouter(
    prefix='/passports',
    tags=['Passports of Traffic Light Objects'],
    # dependencies=[Depends(check_user_is_active)],
)


@router.get(
    '/ovim/',
    status_code=status.HTTP_200_OK,
)
async def get_passports_ovim(
    session:  db_session,
):
    return await OvimPassportsCrud.get_all(session)


@router.get(
    '/ovim/',
    status_code=status.HTTP_200_OK,
)
async def get_passports_ovim(
    session:  db_session,
):
    return await OvimPassportsCrud.get_all(session)


@router.post(
    '/ovim/',
    status_code=status.HTTP_201_CREATED,
)
async def capture_editing_passport_ovim(
    session:  db_session,
    passport: CapturePassport,
):
    return await OvimPassportsCrud.capture_passport(session, passport)


@router.patch(
    '/ovim/',
    status_code=status.HTTP_202_ACCEPTED,
    response_model=SavedPassportSchema,
)
async def save_passport_ovim(
    session:  db_session,
    passport: SavePassport,
) -> SavedPassportSchema:
    res = await OvimPassportsCrud.save_passport(session, passport)
    return SavedPassportSchema.model_validate(res, from_attributes=True)
