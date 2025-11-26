from typing import Annotated

from fastapi.params import Depends
from sqlalchemy.ext.asyncio.session import AsyncSession

from application.interfaces.use_cases.base_crud import BaseCrudUseCaseProtocol
from application.use_cases.base_crud import BaseCrudUseCaseImpl
from infra.database.api import db_api
from infra.database.tlo_repository import TrafficLightObjectSqlAlchemy


# use-cases

db_session = Annotated[
    AsyncSession,
    Depends(db_api.session_getter),
]

def get_tlo() -> BaseCrudUseCaseProtocol:
    return BaseCrudUseCaseImpl(repository=TrafficLightObjectSqlAlchemy(session=db_session))

CrudTloUseCase = Annotated[BaseCrudUseCaseProtocol, Depends(get_tlo)]