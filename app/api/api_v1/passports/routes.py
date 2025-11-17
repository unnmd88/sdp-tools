from typing import Annotated

from fastapi import APIRouter
from pydantic import Field

from starlette import status

from api.api_v1.passport_groups.crud import PassportGroupsCrud
from api.api_v1.passports.crud import PassportsCrud
from api.api_v1.passports.dependencies import passport_group_found_or_404, current_passport_or_404
from api.api_v1.passports.filters import (
    PassportGroupNameFilter,
    PassportCurrentFilter
)
from api.api_v1.passports.schemas import (
    SavePassport,
    CapturePassport,
    SavedPassportSchema,
    CapturedPassport,
    CurrentPassportSchema,
)
from core.constants import PassportGroupsRoutes

from core.dependencies import db_session

router = APIRouter(
    prefix='/passports',
    tags=['Passports of Traffic Light Objects'],
    # dependencies=[Depends(check_user_is_active)],
)


@router.get(
    '/{group_name}/{tlo_id}',
    status_code=status.HTTP_200_OK,
    response_model=CurrentPassportSchema,
)
async def get_valid_passport(
    group_name: PassportGroupsRoutes,
    tlo_id: Annotated[int, Field(ge=1)],
    session: db_session,
) -> CurrentPassportSchema:
    sequence_group_id = await PassportGroupsCrud.get_all(
        session=session,
        filters=PassportGroupNameFilter(group_name_route=group_name),
    )
    passport_group_found_or_404(sequence_group_id=sequence_group_id)
    current_passport = await PassportsCrud.get_all(
        session,
        filters=PassportCurrentFilter(
            group_id=sequence_group_id[-1].id,
            tlo_id=tlo_id,
        ),
    )
    current_passport_or_404(current_passport)
    return CurrentPassportSchema.model_validate(
        current_passport[-1],
        from_attributes=True,
    )





# @router.get(
#     '/{group_name}',
#     status_code=status.HTTP_200_OK,
# )
# async def get_all_passports(
#     session: db_session,
#     group_name_route: PassportGroupsRoutes,
# ):
#     group = await PassportGroupsCrud.get_all(
#         session=session,
#         filters=PassportGroupNameFilter(group_name_route=group_name_route),
#     )
#     if not group:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail='Group not found',
#         )
#
#     return await PassportsCrud.get_all(
#         session,
#         filters=PassportGroupIdFilter(group_id=group[-1].id),
#     )


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=CapturedPassport,
)
async def capture_passport_for_editing(
    session: db_session,
    passport: CapturePassport,
) -> CapturedPassport:
    return await PassportsCrud.capture_passport(session, passport)


@router.patch(
    '/',
    status_code=status.HTTP_202_ACCEPTED,
    response_model=SavedPassportSchema,
)
async def save_passport(
    session: db_session,
    passport: SavePassport,
) -> SavedPassportSchema:
    return await PassportsCrud.save_passport(session, passport)
    return SavedPassportSchema.model_validate(res, from_attributes=True)
