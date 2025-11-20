from collections.abc import Sequence

from fastapi import HTTPException
from sqlalchemy.engine.row import RowMapping
from starlette import status

from api.api_v1.passports.schemas import CurrentPassportSchema


def create_current_passport_schema_or_404(
    db_rows_from_mappings: Sequence[RowMapping],
):
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

        return CurrentPassportSchema(**db_rows_from_mappings[0])
    elif len(db_rows_from_mappings) == 2:
        first, second = db_rows_from_mappings[0], db_rows_from_mappings[1]
        if first['editing_now']:
            return CurrentPassportSchema(
                tlo_name=second['tlo_name'],
                region_code=second['region_code'],
                region_name=second['region_name'],
                street=second['street'],
                service_organization=second['service_organization'],
                username=second['username'],
                passport_group_name=second['passport_group_name'],
                data=second['data'],
                commit_message=second['commit_message'],
                editing_now={'editing_now_by_user': first['username']},
                started_editing_at=second['started_editing_at'],
                finished_editing_at=second['finished_editing_at'],
            )
        return CurrentPassportSchema(
            tlo_name=first['tlo_name'],
            username=first['username'],
            region_code=first['region_code'],
            region_name=first['region_name'],
            street=first['street'],
            service_organization=first['service_organization'],
            passport_group_name=first['passport_group_name'],
            data=first['data'],
            commit_message=first['commit_message'],
            editing_now=first['editing_now'],
            started_editing_at=first['started_editing_at'],
            finished_editing_at=first['finished_editing_at'],
        )
