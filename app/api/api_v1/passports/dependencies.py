from collections.abc import Sequence

from fastapi import HTTPException
from pydantic import BaseModel
from starlette import status

from core.database.crud import T as T_Model


def check_allow_to_save_or_raise_http_exc(
    editable_db_passport: T_Model,
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
    if editable_db_passport.id != model_to_save.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Invalid passport id',
        )

    return True


def passport_group_found_or_404(
    sequence_group_id: Sequence[T_Model],
):
    if len(sequence_group_id) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='No passport found in this group',
        )
    elif len(sequence_group_id) > 1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Founded more than one group',
        )


def valid_data_from_db_or_404(
    current_passport: Sequence[T_Model],
):
    if len(current_passport) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='No passport found',
        )

    # elif len(current_passport) > 1:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail='Founded more than one passport for this group',
    #     )