from fastapi import APIRouter

from fastapi.exceptions import HTTPException
from starlette import status

from presentation.api.api_v1.documentation.regions.endpoints import (
    PATCH_region_by_code_description,
    GET_region_by_code_description,
    DELETE_region_by_code_description,
    POST_region_description,
    GET_region_by_id_description,
    GET_all_regions_description,
)
from presentation.api.dependencies.ioc import ReadRegionUseCase

from presentation.schemas.update import UpdatedRecordSchemaResponse
from presentation.schemas.regions import (
    RegionCreateSchema,
    RegionSchemaResponse,
    RegionUpdate,
)
from application.dto.common import (
    FiltersForSearchDTO,
    ToUpdateRecordDTO,
    CreateRecordDTO,
)

router = APIRouter(
    prefix="/regions",
    tags=["Regions of Traffic Light Objects"],
)


@router.get(
    '/code-or-name/{code-or-name}',
    response_model=RegionSchemaResponse,
    status_code=status.HTTP_200_OK,
)
async def get_region_by_code_or_name(
    code_or_name: str | int,
    read_region_use_case: ReadRegionUseCase,
) -> RegionSchemaResponse:
    return RegionSchemaResponse.model_validate(
        await read_region_use_case.by_code_or_name(code_or_name),
        from_attributes=True,
    )


@router.get(
    "/{id}",
    response_model=RegionSchemaResponse,
    status_code=status.HTTP_200_OK,
    summary="Получить данные региона светофорного объекта по id",
    description=GET_region_by_id_description,
)
async def get_region_by_id(
    id: int,
    read_region_use_case: ReadRegionUseCase,
) -> RegionSchemaResponse:
    return RegionSchemaResponse.model_validate(
        await read_region_use_case.by_id(id),
        from_attributes=True,
    )


@router.get(
    "/",
    response_model=list[RegionSchemaResponse],
    status_code=status.HTTP_200_OK,
    summary="Список всех имеющихся регионов светофорного объекта",
    description=GET_all_regions_description,
)
async def get_all_regions(read_region_use_case: ReadRegionUseCase):
    return [
        RegionSchemaResponse.model_validate(r, from_attributes=True)
        for r in await read_region_use_case.get_many()
    ]
#
#
# @router.post(
#     "/",
#     status_code=status.HTTP_201_CREATED,
#     response_model=RegionSchemaResponse,
#     summary="Создать новый регион светофорного объекта",
#     description=POST_region_description,
# )
# async def create_region(
#     region: RegionCreateSchema,
#     # use_case: RegionsCrudUseCase,
# ) -> RegionSchemaResponse:
#     create_model_fields = region.model_dump(exclude_defaults=True, exclude_none=True)
#     dto = CreateRecordDTO(fields=create_model_fields)
#     try:
#         db_region = await use_case.create_region(dto)
#     except (CreateError, CreateErrorAlreadyExists):
#         raise HTTPException(
#             status_code=status.HTTP_409_CONFLICT,
#             detail="Регион с таким названием/кодом уже существует.",
#         )
#     return RegionSchemaResponse.model_validate(
#         db_region, extra="ignore", from_attributes=True
#     )
#
#
# @router.patch(
#     "/{code}",
#     status_code=status.HTTP_202_ACCEPTED,
#     response_model=UpdatedRecordSchemaResponse,
#     summary="Обновить данные существующего региона.",
#     description=PATCH_region_by_code_description,
# )
# async def update_region(
#     region_code: int,
#     update_data: RegionUpdate,
#     # use_case: RegionsCrudUseCase,
# ):
#     dto = ToUpdateRecordDTO(
#         search_criteria=FiltersFactory.get_filters_dict(code=region_code),
#         fields=update_data.model_dump(exclude_unset=True, exclude_none=True),
#     )
#     try:
#         result = await use_case.update_region(dto)
#     except EntityNotFoundError:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Регион {region_code!r} не найден.",
#         )
#     return result
#
#
# @router.delete(
#     "/{code}",
#     status_code=status.HTTP_202_ACCEPTED,
#     response_model=RegionSchemaResponse,
#     summary="Удалить существующий регион.",
#     description=DELETE_region_by_code_description,
# )
# async def delete_region(
#     region_code: int,
#     # use_case: RegionsCrudUseCase,
# ):
#     filters_for_search_dto = FiltersForSearchDTO(
#         search_filters=FiltersFactory.get_filters_dict(code=region_code)
#     )
#     try:
#         result = await use_case.delete_region(filters_for_search_dto)
#     except EntityNotFoundError:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Регион {region_code} не найден.",
#         )
#     return RegionSchemaResponse.model_validate(
#         result,
#         from_attributes=True,
#     )
