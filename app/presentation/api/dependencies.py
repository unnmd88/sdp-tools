from fastapi import Form
from fastapi.security import HTTPBearer

from application.interfaces.services.authentication import AuthenticationUserServiceProtocol
from application.use_cases.auth.auth import AuthUseCaseImpl
from auth.exceptions import InvalidUsernameOrPasswordException, InactiveUserException
from auth.schemas import AuthSchema, TokenInfo

from typing import Annotated

from fastapi.params import Depends
from sqlalchemy.ext.asyncio.session import AsyncSession

from application.interfaces.use_cases.base_crud import BaseCrudUseCaseProtocol
from application.interfaces.use_cases.get_users_repo import UsersRepositoryUseCaseProtocol
from application.use_cases.base_crud import BaseCrudUseCaseImpl
from application.use_cases.users.get_users_from_repo import UsersRepositoryUseCaseImpl
from auth.services.authentication import AuthenticationUserServiceImpl
from core.users.services.get_user import UserServiceImpl
from infrastructure.database.api import db_api
from infrastructure.database.tlo_repository import TrafficLightObjectSqlAlchemy
from infrastructure.database.user_reposirory import UsersRepositorySqlAlchemy
from presentation.api.exceptions import  InactiveUserErrorHttp403, UnauthorizedErrorHttp401

http_bearer = HTTPBearer()


db_session = Annotated[
    AsyncSession,
    Depends(db_api.session_getter),
]

get_jwt_payload_jwt_bearer = ''

# def get_jwt_payload_jwt_bearer(
#     credentials: Annotated[HTTPAuthorizationCredentials, Depends(http_bearer)],
# ):
#     return PayloadJWTSchema(**decode_jwt(credentials.credentials))





# use-cases


def get_tlo() -> BaseCrudUseCaseProtocol:
    return BaseCrudUseCaseImpl(repository=TrafficLightObjectSqlAlchemy(session=db_session))


def users_crud() -> UsersRepositoryUseCaseProtocol:
    return UsersRepositoryUseCaseImpl(UserServiceImpl())


def auth_form(
    username: str = Form(),
    password: str = Form(),
):
    print('1111111111111111111111111')
    return AuthSchema(username=username, password_plain=password)


def get_auth_user_service(
    user_schema: Annotated[AuthSchema, Depends(auth_form)]
) -> AuthenticationUserServiceProtocol:
    print('2222222222222222222222222')
    print(f'user_schema: {user_schema}')
    return AuthenticationUserServiceImpl(UsersRepositorySqlAlchemy, user_schema,)


def get_auth_user_use_case(
    user_service: Annotated[AuthenticationUserServiceProtocol, Depends(get_auth_user_service)]
) -> AuthenticationUserServiceProtocol:
    print('333333333333333333333333333')
    return AuthUseCaseImpl(user_service)


async def auth_user_and_issue_access_and_refresh_jwt(
    user_service: Annotated[AuthenticationUserServiceProtocol, Depends(get_auth_user_service)]
) -> TokenInfo:
    try:
        use_case = AuthUseCaseImpl(user_service)
        return await use_case.auth_and_issue_jwt(refresh=True)
    except InvalidUsernameOrPasswordException:
        raise UnauthorizedErrorHttp401
    except InactiveUserException:
        raise InactiveUserErrorHttp403

    # return AuthUseCaseImpl(user_service)





CrudTloUseCase = Annotated[BaseCrudUseCaseProtocol, Depends(get_tlo)]
UsersCrudUseCase = Annotated[UsersRepositoryUseCaseProtocol, Depends(users_crud)]
AuthUseCase = Annotated[AuthenticationUserServiceProtocol, Depends(get_auth_user_use_case)]
JWT = Annotated[TokenInfo, Depends(auth_user_and_issue_access_and_refresh_jwt)]
