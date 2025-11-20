import logging

from app_logging.dev.config import OVIM_PASSPORTS_LOGGER
from core.constants import PassportGroupsRoutes as PassportGroupsRoutesEnum
from core.database.crud import BaseCrud
from core.database.crud import T as T_Model
from core.models import (
    Passport,
    PassportGroup,
    Region,
    TrafficLightObject,
    User,
)
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api.api_v1.passports.dependencies import check_allow_to_save_or_raise_http_exc
from api.api_v1.passports.schemas import (
    CapturePassportSchemaSaveToDatabase,
    UpdatePassportSchemaSaveToDatabase,
)
from api.api_v1.passports.utils import create_current_passport_schema_or_404


class PassportsCrud(BaseCrud):
    model = Passport
    logger = logging.getLogger(OVIM_PASSPORTS_LOGGER)

    @classmethod
    async def get_current_passport(
        cls,
        session: AsyncSession,
        tlo_name: str,
        group_name_route: PassportGroupsRoutesEnum,
    ):
        stmt = (
            select(
                Passport.user_id.label('passport_user_id'),
                TrafficLightObject.id.label('tlo_id'),
                TrafficLightObject.name.label('tlo_name'),
                TrafficLightObject.street,
                TrafficLightObject.service_organization,
                Region.code.label('region_code'),
                Region.name.label('region_name'),
                PassportGroup.id.label('passport_group_id'),
                PassportGroup.group_name.label('passport_group_name'),
                Passport.id.label('passport_id'),
                Passport.tlo_id,
                Passport.data,
                Passport.commit_message,
                Passport.editing_now,
                Passport.started_editing_at,
                Passport.finished_editing_at,
                User.username.label('username'),
            )
            .where(
                TrafficLightObject.name == tlo_name,
                PassportGroup.group_name_route == group_name_route,
                Passport.tlo_id == TrafficLightObject.id,
                User.id == Passport.user_id,
                Passport.group_id == PassportGroup.id,
                Region.id == TrafficLightObject.region_id,
            )
            .order_by(Passport.finished_editing_at.desc())
            .limit(2)
        )
        result = await session.execute(stmt)
        mappings = result.mappings().all()
        return create_current_passport_schema_or_404(mappings)

    @classmethod
    async def get_last_passport_or_none(
        cls,
        session: AsyncSession,
        tlo_id: int,
    ) -> T_Model | None:
        stmt = (
            select(cls.model)
            .where(cls.model.tlo_id == tlo_id)
            .order_by(cls.model.started_editing_at.desc())
            .limit(1)
        )
        return await session.scalar(stmt)

    @classmethod
    async def capture_passport(
        cls,
        session: AsyncSession,
        model: CapturePassportSchemaSaveToDatabase,
    ):
        last_passport: T_Model = await cls.get_last_passport_or_none(
            session, model.tlo_id
        )
        if last_passport is not None and last_passport.editing_now:
            if last_passport.user_id == model.user_id:
                return last_passport
            else:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f'Passport is edited by user with id={last_passport.user_id}',
                )
        return await cls.add(session, model)

    @classmethod
    async def save_passport(
        cls,
        session: AsyncSession,
        model: UpdatePassportSchemaSaveToDatabase,
    ):
        editable_db_passport = await cls.get_last_passport_or_none(
            session, model.tlo_id
        )
        check_allow_to_save_or_raise_http_exc(
            editable_db_passport=editable_db_passport,
            model_to_save=model,
        )
        return await cls.update(
            session,
            editable_db_passport,
            model,
        )
