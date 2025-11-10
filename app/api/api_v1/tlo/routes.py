from typing import Annotated

from fastapi import (
    APIRouter, Depends,
)
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.tlo.crud import TloCrud
from auth.token_validation import check_user_is_active

from core.database import db_api

router = APIRouter(
    prefix="/traffic-light-objects",
    tags=['Traffic-light-objects'],
    # dependencies=[Depends(check_user_is_active)],
)


@router.get('/{id}')
async def get_traffic_light_object_by_id(
    pk_id: int,
    session: Annotated[
        AsyncSession,
        Depends(db_api.session_getter)
    ]
):
    return await TloCrud.get_one_by_id_or_404(session, pk_id)


@router.get('/')
async def get_traffic_light_objects(
    session: Annotated[
        AsyncSession,
        Depends(db_api.session_getter)
    ]
):
    return await TloCrud.get_all(session)

