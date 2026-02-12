from typing import Annotated

# from domain.database import db_api
from fastapi import (
    APIRouter,
    Depends,
)
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from application.use_cases.tlo_use_cases.types import TrafficLightObjectsReadUseCase, TrafficLightObjectsCreateUseCase
from domain.traffic_light_objects.tlo_commands import CreateTrafficLightObjectCommand
from presentation.api.api_v1.tlo.schemas import (
    TrafficLightCreate,
    TrafficLightSchema,
    TrafficLightUpdate,
)

from dishka.integrations.fastapi import FromDishka, inject

from presentation.api.fastapi_dependencies import AccessTokenDep
from presentation.schemas.traffic_light_objects import TrafficLightObjectCreate

router = APIRouter(
    prefix="/traffic-light-objects",
    tags=["Traffic Light Objects"],
    # dependencies=[Depends(check_user_is_active)],
)


@router.get("/as-tets-ddd/{id}")
async def get_traffic_light_object_by_id(
    tlo_id: int,
    # use_case: CrudTloUseCase,
    # session: Annotated[AsyncSession, Depends(db_api.session_getter)],
):
    return await use_case.get_by_id(tlo_id)
    # return await TloCrud.get_one_by_id_or_404(session, traffic_light_object_id)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
)
@inject
async def get_list_traffic_light_objects(
    use_case: FromDishka[TrafficLightObjectsReadUseCase],
):
    return await use_case.get_many()
    return RegionResponse.model_validate(
        await read_region_use_case(code_or_name),
        from_attributes=True,
    )


@router.get("/{id}")
async def get_traffic_light_object_by_id(
    traffic_light_object_id: int,
    # session: Annotated[AsyncSession, Depends(db_api.session_getter)],
):
    return await TloCrud.get_one_by_id_or_404(session, traffic_light_object_id)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    # response_model=TrafficLightSchema,
)
@inject
async def create_traffic_light_object(
    token_dto: AccessTokenDep,
    new_traffic_light_object_schema: TrafficLightObjectCreate,
    use_case: FromDishka[TrafficLightObjectsCreateUseCase],
):
    command = CreateTrafficLightObjectCommand(
        customer_id=token_dto.user_id,
        region_id=new_traffic_light_object_schema.region_id,
        name=new_traffic_light_object_schema.name,
        created_by_user_id=token_dto.user_id,
        updated_by_user_id=token_dto.user_id,
        traffic_controller_type=new_traffic_light_object_schema.traffic_controller_type,
        latitude=new_traffic_light_object_schema.latitude,
        longitude=new_traffic_light_object_schema.longitude,
        district=new_traffic_light_object_schema.district,
        address=new_traffic_light_object_schema.address,
        note=new_traffic_light_object_schema.note,
    )
    await use_case(command)


@router.patch(
    "/{id}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=TrafficLightSchema,
)
async def update_traffic_light_object(
    traffic_light_object_id: int,
    traffic_light_object: TrafficLightUpdate,
    # session: Annotated[AsyncSession, Depends(db_api.session_getter)],
) -> TrafficLightSchema:
    tlo = await TloCrud.get_one_by_id_or_404(session, traffic_light_object_id)
    updated_traffic_light_object = await TloCrud.update_by_id(
        session=session,
        db_model=tlo,
        to_update_model=traffic_light_object,
    )
    return TrafficLightSchema.model_validate(
        updated_traffic_light_object,
        from_attributes=True,
    )
