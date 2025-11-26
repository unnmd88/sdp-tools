from collections.abc import Sequence

from fastapi import HTTPException
from sqlalchemy.engine.row import RowMapping
from starlette import status

from presentation.api.api_v1.passports.schemas import CurrentPassportSchema


def create_current_passport_schema_or_404(
    db_rows_from_mappings: Sequence[RowMapping],
):
    if len(db_rows_from_mappings) == 2:
        first, second = dict(db_rows_from_mappings[0]), dict(db_rows_from_mappings[1])
        if first['editing_now']:
            second.update(editing_now={'editing_now_by_user': first['username']})
            current_passport = second
        else:
            current_passport = first
        return CurrentPassportSchema(**current_passport)
    elif len(db_rows_from_mappings) == 1:
        if db_rows_from_mappings[0]['editing_now']:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Has not current passport, but '
                       f'editing now by user={db_rows_from_mappings[0]["username"]}',
            )
        return CurrentPassportSchema(**db_rows_from_mappings[0])

    if not db_rows_from_mappings:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Current passport not found',
        )
    elif len(db_rows_from_mappings) == 1:
        if db_rows_from_mappings[0]['editing_now']:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Has not current passport, but '
                       f'editing now by user={db_rows_from_mappings[0]["username"]}',
            )
    raise ValueError('Count rows should be no more than 2')
