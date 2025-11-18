import logging
from typing import Annotated

from fastapi import HTTPException
from pydantic import Field

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api.api_v1.passports.dependencies import check_allow_to_save_or_raise_http_exc
from api.api_v1.passports.schemas import CapturePassportSchema, UpdatePassport, CapturePassportSchemaSaveToDatabase, \
    UpdatePassportSchemaSaveToDatabase
from app_logging.dev.config import OVIM_PASSPORTS_LOGGER
from core.database.crud import BaseCrud, T as T_Model
from core.models import Passport


class PassportsCrud(BaseCrud):

    model = Passport
    logger = logging.getLogger(OVIM_PASSPORTS_LOGGER)


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
            session,
            model.tlo_id
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
            session,
            model.tlo_id
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

    # @classmethod
    # async def save_passport(
    #         cls,
    #         session: AsyncSession,
    #         model: SavePassport,
    # ):
    #     if (db_passport := await cls.get_last_passport_or_none(session, model.tlo_id)) is None:
    #         raise HTTPException(
    #             status_code=status.HTTP_404_NOT_FOUND,
    #             detail=f'Invalid Traffic light id',
    #         )
    #     if db_passport.user_id != model.user_id:
    #         raise HTTPException(
    #             status_code=status.HTTP_409_CONFLICT,
    #             detail=f'Passport is edited by user with id={db_passport.user_id}',
    #         )
    #     if not db_passport.editing_now:
    #         raise HTTPException(
    #             status_code=status.HTTP_404_NOT_FOUND,
    #             detail=f'Passport editing not found. Please capture passport for editing.',
    #         )
    #     return await cls.update(
    #         session,
    #         db_passport,
    #         model,
    #     )


# class PassportsCrud(ProxyPassportsCrud):
#     model = Passport
#     logger = logging.getLogger(OVIM_PASSPORTS_LOGGER)
