from fastapi import APIRouter

from fastapi.exceptions import HTTPException
from starlette import status

from core.dto.regions import CreateRegionsDTO, UpdateRegionsDTO
from core.enums import RegionNames
from core.exceptions.base import CreateError
from core.users.exceptions import DomainValidationError
from presentation.schemas.regions import (
    RegionCreate,
    RegionSchema,
    RegionUpdate,
)
from presentation.api.dependencies.deps import RegionsCrudUseCase, UserEntityDep

router = APIRouter(
    prefix='/regions',
    tags=['Regions of Traffic Light Objects'],
)


@router.get('/code/{code}')
async def get_region_by_code(
    code: int,
):
    raise NotImplemented


@router.get('/name/{name}')
async def get_region_by_name(
    name: str,
):
    raise NotImplemented


@router.get(
    '/{id}',
    response_model=RegionSchema,
    status_code=status.HTTP_200_OK,
)
async def get_region_by_id(
    region_id: int,
    use_case: RegionsCrudUseCase,
):

    if (region := await use_case.get_region_by_id(region_id)) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Регион с id={region_id} не найден.'
        )
    return  RegionSchema.model_validate(region, from_attributes=True)


@router.get(
    '/',
    response_model=list[RegionSchema],
    status_code=status.HTTP_200_OK,
)
async def get_regions(
    use_case: RegionsCrudUseCase,
):
    return await use_case.get_all_regions()
# async def get_regions(session: Annotated[AsyncSession, Depends(db_api.session_getter)]):
#     return await RegionsCrud.get_all(session)


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=RegionSchema,
)
async def create_region(
    region: RegionCreate,
    use_case: RegionsCrudUseCase,
) -> RegionSchema:
    dto = CreateRegionsDTO(**region.model_dump())
    try:
        db_region = await use_case.create_region(dto)
    except CreateError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Регион уже существует',
        )
    return RegionSchema.model_validate(db_region, extra='ignore', from_attributes=True)


@router.patch(
    '/',
    status_code=status.HTTP_202_ACCEPTED,
    # response_model=RegionSchema,
)
async def update_region(
    update_data: RegionUpdate,
    use_case: RegionsCrudUseCase,
    # session: Annotated[AsyncSession, Depends(db_api.session_getter)],
):
    dto = UpdateRegionsDTO(**update_data.model_dump())
    return await use_case.update_region(dto)

    db_region = await RegionsCrud.get_one_by_id_or_404(session, region_id)
    updated_region = await RegionsCrud.update(session, db_region, region)
    return RegionSchema.model_validate(
        updated_region, extra='ignore', from_attributes=True
    )
