from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
)
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api.api_v1.passports.crud import OvimPassportsCrud
from api.api_v1.passports.schemas import CreatePassport
from api.api_v1.regions.crud import RegionsCrud
from api.api_v1.tlo.crud import TloCrud
from api.api_v1.tlo.schemas import TrafficLightCreate, TrafficLightSchema, TrafficLightUpdate

from core.database import db_api
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


@router.post(
    '/ovim/',
    status_code=status.HTTP_201_CREATED,
)
async def create_passport_ovim(
    session:  db_session,
    passport: CreatePassport,
):

    return await OvimPassportsCrud.add(session, passport)