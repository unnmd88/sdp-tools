from typing import Annotated

from fastapi import APIRouter, Depends

from fastapi.exceptions import HTTPException
from starlette import status

from core.dto.regions import CreateRegionDTO, UpdateRegionDTO
from core.exceptions.base import (
    CreateError,
    CreateErrorAlreadyExists,
    NotFoundError,
)
from presentation.api.dependencies.utils import get_filters_for_region_or_name_search
from presentation.schemas.regions import (
    RegionCreate,
    RegionSchema,
    RegionUpdate,
)
from presentation.api.dependencies.deps import RegionsCrudUseCase, regions_filters_for_search
from presentation.schemas.update import UpdatedEntitySchemaResponse

router = APIRouter(
    prefix='/regions',
    tags=['Regions of Traffic Light Objects'],
)


@router.get(
    '/{code-or-name}',
    response_model=RegionSchema,
    status_code=status.HTTP_200_OK,
)
async def get_region_by_code_or_name(
    code_or_name: str,
    use_case: RegionsCrudUseCase,
):
    filters_for_search_dto = get_filters_for_region_or_name_search(code_or_name)
    if (region := await use_case.get_region_by_filters(filters_for_search_dto)) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Регион {code_or_name!r} не найден.'
        )
    return RegionSchema.model_validate(region, from_attributes=True)


@router.get(
    '/id/{id}',
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
async def get_list_regions(
    use_case: RegionsCrudUseCase,
):
    return await use_case.get_all_regions()



@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=RegionSchema,
)
async def create_region(
    region: RegionCreate,
    use_case: RegionsCrudUseCase,
) -> RegionSchema:
    dto = CreateRegionDTO(**region.model_dump())
    try:
        db_region = await use_case.create_region(dto)
    except (CreateError, CreateErrorAlreadyExists):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Регион с таким названием/кодом уже существует',
        )
    return RegionSchema.model_validate(db_region, extra='ignore', from_attributes=True)


@router.patch(
    '/',
    status_code=status.HTTP_202_ACCEPTED,
    response_model=UpdatedEntitySchemaResponse,
)
async def update_region(
    update_data: RegionUpdate,
    use_case: RegionsCrudUseCase,
):
    dto = UpdateRegionDTO(
        filters_for_search=get_filters_for_region_or_name_search(update_data.code_or_name).filters_for_search,
        code_or_name=update_data.code_or_name,
        code=update_data.code,
        name=update_data.name,
    )
    try:
        result = await use_case.update_region(dto)
        return UpdatedEntitySchemaResponse.model_validate(
            result,
            from_attributes=True,
        )
    except NotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Регион с id={dto.id} не найден.'
        )

@router.delete(
    '/{id}',
    status_code=status.HTTP_202_ACCEPTED,
    response_model=RegionSchema,
)
async def delete_region(
    region_id: int,
    use_case: RegionsCrudUseCase,
):
    try:
        result = await use_case.delete_region(region_id)
        return RegionSchema.model_validate(
            result,
            from_attributes=True,
        )
    except NotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Регион с id={region_id} не найден.'
        )