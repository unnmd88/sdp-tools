from typing import Annotated

from annotated_types import MinLen
from auth.schemas import PayloadJWTSchema
from auth.token_validation import check_user_is_active
from core.constants import PassportGroupsRoutes
# from core.dependencies import db_session
from infrastructure.database.models import PassportGroup as PassportGroupModel
from infrastructure.database.models import TrafficLightObject
from fastapi import APIRouter, Depends
from starlette import status

from presentation.api.api_v1.passports.crud import PassportsCrud
from presentation.api.api_v1.passports.dependencies import (
    passport_group_found_or_404,
    valid_data_from_db_or_404,
)
from presentation.api.api_v1.passports.filters import (
    PassportCurrentFilter,
)
from presentation.api.api_v1.passports.schemas import (
    CapturedPassport,
    CapturePassportSchema,
    CapturePassportSchemaSaveToDatabase,
    FinalSavedPassportSchema,
    UpdatePassport,
    UpdatePassportSchemaSaveToDatabase,
)
from presentation.api.dependencies import get_jwt_payload_jwt_bearer, db_session

router = APIRouter(
    prefix='/passports',
    tags=['Passports of Traffic Light Objects'],
    dependencies=[Depends(check_user_is_active)],
)


@router.get(
    '/{group_name}/{tlo_name}',
    status_code=status.HTTP_200_OK,
    # response_model=CurrentPassportSchema,
)
async def get_valid_passport(
    group_name: PassportGroupsRoutes,
    tlo_name: Annotated[str, MinLen(1)],
    session: db_session,
    user_data: Annotated[PayloadJWTSchema, Depends(get_jwt_payload_jwt_bearer)],
    # ) -> CurrentPassportSchema:
):
    return await PassportsCrud.get_current_passport(
        session=session,
        group_name_route=group_name,
        tlo_name=tlo_name,
    )

    tlo_id = await PassportGroupsCrud.get_pk_id_from_model_or_404(
        session=session,
        from_model=TrafficLightObject,
        name=tlo_name,
    )
    group_id = await PassportGroupsCrud.get_pk_id_from_model_or_404(
        session=session,
        from_model=PassportGroupModel,
        group_name=group_name,
    )

    sequence_group_id = await PassportGroupsCrud.get_all(
        session=session,
        filters=PassportCurrentFilter(
            group_id=group_id,
            tlo_id=tlo_id,
        ),
    )
    passport_group_found_or_404(sequence_group_id=sequence_group_id)
    all_passports_this_tlo_name = await PassportsCrud.get_all(
        session,
        filters=PassportCurrentFilter(
            group_id=sequence_group_id[-1].id,
            tlo_id=tlo_name,
        ),
    )
    valid_data_from_db_or_404(all_passports_this_tlo_name)
    current_passport = all_passports_this_tlo_name[-1]
    user = await PassportGroupsCrud.get_user_by_id_or_404(
        session=session,
        user_id=current_passport.user_id,
    )


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=CapturedPassport,
)
async def capture_for_editing(
    session: db_session,
    passport: CapturePassportSchema,
    user_data: Annotated[PayloadJWTSchema, Depends(get_jwt_payload_jwt_bearer)],
) -> CapturedPassport:
    # ) :
    tlo_id = await PassportsCrud.get_pk_id_from_model_or_404(
        session=session,
        from_model=TrafficLightObject,
        name=passport.tlo_name,
    )
    group_id = await PassportsCrud.get_pk_id_from_model_or_404(
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
        ),
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
    user_data: Annotated[PayloadJWTSchema, Depends(get_jwt_payload_jwt_bearer)],
) -> FinalSavedPassportSchema:
    tlo_id = await PassportsCrud.get_pk_id_from_model_or_404(
        session=session,
        from_model=TrafficLightObject,
        name=passport.tlo_name,
    )
    group_id = await PassportsCrud.get_pk_id_from_model_or_404(
        session=session,
        from_model=PassportGroupModel,
        group_name=passport.group_name,
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
        ),
    )
    return FinalSavedPassportSchema(
        id=passport_db.id,
        tlo_name=passport.tlo_name,
        group_name=passport.group_name,
        username=user_data.sub,
        editing_now=passport_db.editing_now,
    )
    return FinalSavedPassportSchema.model_validate(res, from_attributes=True)
