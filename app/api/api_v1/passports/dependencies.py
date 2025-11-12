from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from core.database.crud import T
from core.models import OvimPassport


def check_allow_to_save_or_raise_http_exc(
    editable_db_passport: T,
    model_to_save: BaseModel,
):
    if editable_db_passport is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Invalid Traffic light id',
        )
    if editable_db_passport.user_id != model_to_save.user_id:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f'Passport is edited by user with id={editable_db_passport.user_id}',
        )
    if not editable_db_passport.editing_now:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Passport editing not found. Please capture passport for editing.',
        )
    return True


