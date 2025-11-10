from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
)
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.regions.crud import RegionsCrud
from api.api_v1.regions.schemas import CreateRegionSchema, RegionSchema
from core.database import db_api

router = APIRouter(
    prefix='/regions',
    tags=['Regions-of-traffic-light-objects'],
)


@router.get('/code-or-name/{code_or_name}')
async def get_region_by_code_or_name(
    code_or_name: int | str,
    session: Annotated[AsyncSession, Depends(db_api.session_getter)],
):
    return await RegionsCrud.get_one_by_code_or_name_or_404(session, code_or_name)


@router.get('/{id}')
async def get_region_by_id(
    num_id: int, session: Annotated[AsyncSession, Depends(db_api.session_getter)]
):
    return await RegionsCrud.get_one_by_id_or_404(session, num_id)


@router.get('/')
async def get_regions(session: Annotated[AsyncSession, Depends(db_api.session_getter)]):
    return await RegionsCrud.get_all(session)


@router.post(
    '/',
    status_code=201,
    response_model=RegionSchema,
)
async def create_region(
    region: CreateRegionSchema,
    session: Annotated[AsyncSession, Depends(db_api.session_getter)],
) -> RegionSchema:
    db_region = await RegionsCrud.add(session, region)
    return RegionSchema.model_validate(db_region, extra='ignore', from_attributes=True)
