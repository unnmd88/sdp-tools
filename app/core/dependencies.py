from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import db_api

db_session = Annotated[
    AsyncSession,
    Depends(db_api.session_getter),
]