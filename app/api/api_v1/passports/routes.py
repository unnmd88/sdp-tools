from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import Field

from starlette import status

from api.api_v1.passport_groups.crud import PassportGroupsCrud
from api.api_v1.passports.crud import PassportsCrud
from api.api_v1.passports.dependencies import passport_group_found_or_404, current_passport_or_404
from api.api_v1.passports.filters import (
    PassportGroupNameRouteFilter,
    PassportCurrentFilter, PassportGroupNameFilter
)
from api.api_v1.passports.schemas import (
    UpdatePassport,
    CapturePassportSchema,
    FinalSavedPassportSchema,
    CapturedPassport,
    CurrentPassportSchema, CapturePassportSchemaSaveToDatabase, UpdatePassportSchemaSaveToDatabase,
)
from api.dependencies import http_bearer, get_jwt_payload_jwt_bearer
from auth.schemas import PayloadJWTSchema
from auth.token_validation import check_user_is_active
from core.constants import PassportGroupsRoutes, PassportGroups

from core.dependencies import db_session
from core.models import PassportGroup as PassportGroupModel, TrafficLightObject

router = APIRouter(
    prefix='/passports',
    tags=['Passports of Traffic Light Objects'],
    dependencies=[Depends(check_user_is_active)],
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
        filters=PassportGroupNameRouteFilter(group_name_route=group_name),
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


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,

    response_model=CapturedPassport,
)
async def capture_for_editing(
    session: db_session,
    passport: CapturePassportSchema,
    user_data: Annotated[PayloadJWTSchema, Depends(get_jwt_payload_jwt_bearer)]
) -> CapturedPassport:
# ) :
    tlo_id = await PassportGroupsCrud.get_pk_id_from_model_or_404(
        session=session,
        from_model=TrafficLightObject,
        name=passport.tlo_name,
    )
    group_id = await PassportGroupsCrud.get_pk_id_from_model_or_404(
        session=session,
        from_model=PassportGroupModel,
        group_name=passport.group_name,
    )
    passport_db = await PassportsCrud.capture_passport(
        session,
        CapturePassportSchemaSaveToDatabase(
            tlo_id=tlo_id,
            group_id=group_id,
            user_id=user_data.user_id,
        )
    )
    return CapturedPassport(
        id=passport_db.id,
        tlo_name=passport.tlo_name,
        group_name=passport.group_name,
        username=user_data.sub,
        editing_now=passport_db.editing_now,
    )


@router.patch(
    '/',
    status_code=status.HTTP_202_ACCEPTED,
    response_model=FinalSavedPassportSchema,
)
async def save_passport(
    session: db_session,
    passport: UpdatePassport,
    user_data: Annotated[PayloadJWTSchema, Depends(get_jwt_payload_jwt_bearer)]
) -> FinalSavedPassportSchema:
    tlo_id = await PassportGroupsCrud.get_pk_id_from_model_or_404(
        session=session,
        from_model=TrafficLightObject,
        name=passport.tlo_name,
    )
    group_id = await PassportGroupsCrud.get_pk_id_from_model_or_404(
        session=session,
        from_model=PassportGroupModel,
        group_name=passport.group_name,
    )
    passport_db = await PassportsCrud.capture_passport(
        session,
        CapturePassportSchemaSaveToDatabase(
            tlo_id=tlo_id,
            group_id=group_id,
            user_id=user_data.user_id,
        )
    )
    passport_db = await PassportsCrud.save_passport(
        session,
        UpdatePassportSchemaSaveToDatabase(
            id=passport.id,
            user_id=user_data.user_id,
            tlo_id=tlo_id,
            group_id=group_id,
            data=passport.data,
            commit_message=passport.commit_message,
        )
    )
    return FinalSavedPassportSchema(
        id=passport_db.id,
        tlo_name=passport.tlo_name,
        group_name=passport.group_name,
        username=user_data.sub,
        editing_now=passport_db.editing_now,
    )
    return FinalSavedPassportSchema.model_validate(res, from_attributes=True)
