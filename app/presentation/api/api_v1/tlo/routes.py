from typing import Annotated

# from core.database import db_api
from fastapi import (
    APIRouter,
    Depends,
)
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from application.dependencies import CrudTloUseCase
from presentation.api.api_v1.regions.crud import RegionsCrud
from presentation.api.api_v1.tlo.crud import TloCrud
from presentation.api.api_v1.tlo.schemas import (
    TrafficLightCreate,
    TrafficLightSchema,
    TrafficLightUpdate,
)
from infrastructure.database.api import db_api

router = APIRouter(
    prefix='/traffic-light-objects',
    tags=['Traffic Light Objects'],
    # dependencies=[Depends(check_user_is_active)],
)

@router.get('/as-tets-ddd/{id}')
async def get_traffic_light_object_by_id(
    tlo_id: int,
    use_case: CrudTloUseCase,
    session: Annotated[AsyncSession, Depends(db_api.session_getter)],
):
    return await use_case.get_one_by_id(tlo_id)
    # return await TloCrud.get_one_by_id_or_404(session, traffic_light_object_id)


@router.get('/{id}')
async def get_traffic_light_object_by_id(
    traffic_light_object_id: int,
    session: Annotated[AsyncSession, Depends(db_api.session_getter)],
):
    return await TloCrud.get_one_by_id_or_404(session, traffic_light_object_id)


@router.get('/')
async def get_traffic_light_objects(
    session: Annotated[AsyncSession, Depends(db_api.session_getter)],
):
    return await TloCrud.get_all(session)


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=TrafficLightSchema,
)
async def create_traffic_light_object(
    traffic_light_object: TrafficLightCreate,
    session: Annotated[AsyncSession, Depends(db_api.session_getter)],
) -> TrafficLightSchema:
    await RegionsCrud.get_one_by_id_or_404(session, traffic_light_object.region_id)
    tlo = await TloCrud.add(session, traffic_light_object)
    return TrafficLightSchema.model_validate(tlo, from_attributes=True)


@router.patch(
    '/{id}',
    status_code=status.HTTP_202_ACCEPTED,
    response_model=TrafficLightSchema,
)
async def update_traffic_light_object(
    traffic_light_object_id: int,
    traffic_light_object: TrafficLightUpdate,
    session: Annotated[AsyncSession, Depends(db_api.session_getter)],
) -> TrafficLightSchema:
    tlo = await TloCrud.get_one_by_id_or_404(session, traffic_light_object_id)
    updated_traffic_light_object = await TloCrud.update(
        session=session,
        db_model=tlo,
        to_update_model=traffic_light_object,
    )
    return TrafficLightSchema.model_validate(
        updated_traffic_light_object,
        from_attributes=True,
    )
