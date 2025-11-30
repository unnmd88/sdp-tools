# from typing import Annotated
#
# from fastapi.params import Depends
# from sqlalchemy.ext.asyncio.session import AsyncSession
#
# from application.interfaces.use_cases.base_crud import BaseCrudUseCaseProtocol
# from application.interfaces.use_cases.get_users_repo import UsersRepositoryUseCaseProtocol
# from application.use_cases.base_crud import BaseCrudUseCaseImpl
# from application.use_cases.users.get_users_from_repo import UsersRepositoryUseCaseImpl
# from core.users.services.get_user import UserServiceImpl
# from infrastructure.database.api import db_api
# from infrastructure.database.tlo_repository import TrafficLightObjectSqlAlchemy
# from infrastructure.database.user_reposirory import UsersRepositorySqlAlchemy
#
# # use-cases
#
# db_session = Annotated[
#     AsyncSession,
#     Depends(db_api.session_getter),
# ]
#
# def get_tlo() -> BaseCrudUseCaseProtocol:
#     return BaseCrudUseCaseImpl(repository=TrafficLightObjectSqlAlchemy(session=db_session))
#
#
# def users_crud() -> UsersRepositoryUseCaseProtocol:
#     return UsersRepositoryUseCaseImpl(UserServiceImpl())
#
#
# CrudTloUseCase = Annotated[BaseCrudUseCaseProtocol, Depends(get_tlo)]
# UsersCrudUseCase = Annotated[UsersRepositoryUseCaseProtocol, Depends(users_crud)]
