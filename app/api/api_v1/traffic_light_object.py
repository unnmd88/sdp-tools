
from fastapi import (
    APIRouter,
)

router = APIRouter(tags=['Traffic-light-objects'])


@router.get('')
async def get_users(
    # session: AsyncSession = Depends(db_helper.session_getter),
    # session: Annotated[
    #     AsyncSession,
    #     Depends(db_helper.session_getter),
    # ],
):
    return {'TLO': 'Traffic-light-objects'}
