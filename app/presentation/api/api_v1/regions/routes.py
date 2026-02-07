from fastapi import APIRouter

from starlette import status

from application.use_cases.regions.create_region_use_case import CreateRegionUseCaseImpl
from application.use_cases.regions.delete_region_use_case import DeleteRegionUseCaseImpl
from application.use_cases.regions.read_region_use_case import ReadRegionUseCaseImpl
from application.use_cases.regions.update_regions_use_case import (
    UpdateRegionUseCaseImpl,
)
from domain.cqrs.region_commands import UpdateRegionCommand, CreateRegionCommand, DeleteRegionCommand
from presentation.api.api_v1.documentation.regions.endpoints import (
    PATCH_region_by_code_description,
    GET_all_regions_description,
)
from presentation.api.fastapi_dependencies import AccessTokenDep

from presentation.schemas.regions import (
    RegionResponse,
    RegionUpdate, RegionCreate,
)
from dishka.integrations.fastapi import FromDishka, inject


router = APIRouter(
    prefix="/regions",
    tags=["Regions of Traffic Light Objects"],
)


@router.get(
    "/{code-or-name}",
    response_model=RegionResponse,
    status_code=status.HTTP_200_OK,
)
@inject
async def get_region_by_code_or_name(
    code_or_name: str | int, read_region_use_case: FromDishka[ReadRegionUseCaseImpl]
) -> RegionResponse:
    return RegionResponse.model_validate(
        await read_region_use_case.by_code_or_name(code_or_name),
        from_attributes=True,
    )


# @router.get(
#     "/{id}",
#     response_model=RegionSchemaResponse,
#     status_code=status.HTTP_200_OK,
#     summary="Получить данные региона светофорного объекта по id",
#     description=GET_region_by_id_description,
# )
# async def get_region_by_id(
#     id: int,
#     read_region_use_case: ReadRegionUseCase,
# ) -> RegionSchemaResponse:
#     return RegionSchemaResponse.model_validate(
#         await read_region_use_case.by_id(id),
#         from_attributes=True,
#     )


@router.get(
    "/",
    response_model=list[RegionResponse],
    status_code=status.HTTP_200_OK,
    summary="Список регионов светофорного объекта",
    description=GET_all_regions_description,
)
@inject
async def get_regions(
    read_region_use_case: FromDishka[ReadRegionUseCaseImpl],
):
    return [
        RegionResponse.model_validate(r, from_attributes=True)
        for r in await read_region_use_case.get_many()
    ]


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=RegionResponse,
    summary="Создать новый регион светофорного объекта",
    # description=POST_region_description,
)
@inject
async def create_region(
    token_dto: AccessTokenDep,
    new_region_schema: RegionCreate,
    use_case: FromDishka[CreateRegionUseCaseImpl],
    # use_case: RegionsCrudUseCase,
) -> RegionResponse:
    command = CreateRegionCommand(
        customer_id=token_dto.user_id,
        **new_region_schema.model_dump()
    )
    return RegionResponse.model_validate(
        await use_case(command),
        from_attributes=True,
    )


    return command
    create_model_fields = region.model_dump(exclude_defaults=True, exclude_none=True)
    dto = CreateRecordDTO(fields=create_model_fields)
    try:
        db_region = await use_case.create_region(dto)
    except (CreateError, CreateErrorAlreadyExists):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Регион с таким названием/кодом уже существует.",
        )
    return RegionSchemaResponse.model_validate(
        db_region, extra="ignore", from_attributes=True
    )


@router.patch(
    "/{code-or-name}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=RegionResponse,
    summary="Обновить данные существующего региона.",
    description=PATCH_region_by_code_description,
)
@inject
async def update_region(
    token_dto: AccessTokenDep,
    code_or_name: str | int,
    update_data: RegionUpdate,
    use_case: FromDishka[UpdateRegionUseCaseImpl],
) -> RegionResponse:
    command = UpdateRegionCommand(
        user_id=token_dto.user_id,
        code_or_name=code_or_name,
        **update_data.model_dump(exclude_unset=True),
    )
    return RegionResponse.model_validate(
        await use_case(command),
        from_attributes=True,
    )




@router.delete(
    "/{code-or-name}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=RegionResponse,
    summary="Удалить существующий регион.",
    # description=DELETE_region_by_code_description,
)
@inject
async def delete_region(
    token_dto: AccessTokenDep,
    code_or_name: str | int,
    use_case: FromDishka[DeleteRegionUseCaseImpl],
):
    command = DeleteRegionCommand(
        customer_id=token_dto.user_id,
        code_or_name=code_or_name,
    )
    return RegionResponse.model_validate(
        await use_case(command),
        from_attributes=True,
    )
