from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
)
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api.api_v1.regions.crud import RegionsCrud
from api.api_v1.regions.schemas import RegionCreate, RegionSchema, RegionUpdate
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


@router.get(
'/{id}',
    response_model=RegionSchema,
    status_code=status.HTTP_200_OK,
)
async def get_region_by_id(
    region_id: int,
    session: Annotated[AsyncSession, Depends(db_api.session_getter)],
):
    return await RegionsCrud.get_one_by_id_or_404(session, region_id)


@router.get(
    '/',
    response_model=list[RegionSchema],
    status_code=status.HTTP_200_OK,
)
async def get_regions(session: Annotated[AsyncSession, Depends(db_api.session_getter)]):
    return await RegionsCrud.get_all(session)


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=RegionSchema,
)
async def create_region(
    region: RegionCreate,
    session: Annotated[AsyncSession, Depends(db_api.session_getter)],
) -> RegionSchema:
    db_region = await RegionsCrud.add(session, region)
    return RegionSchema.model_validate(db_region, extra='ignore', from_attributes=True)


@router.patch(
    '/{id}',
    status_code=status.HTTP_202_ACCEPTED,
    response_model=RegionSchema,
)
async def update_region(
    region_id: int,
    region: RegionUpdate,
    session: Annotated[AsyncSession, Depends(db_api.session_getter)],
) -> RegionSchema:
    db_region = await RegionsCrud.get_one_by_id_or_404(session, region_id)
    updated_region = await RegionsCrud.update(session, db_region, region)
    return RegionSchema.model_validate(updated_region, extra='ignore', from_attributes=True)