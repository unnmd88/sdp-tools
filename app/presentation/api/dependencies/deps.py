from typing import Annotated

from fastapi import Depends
from fastapi.params import Form

from application.use_cases.auth.auth_and_issue_jwt import AuthJWTUseCaseImpl
from application.use_cases.users.crud import UsersCrudUseCaseImpl
from presentation.api.dependencies.dependencies import (
    auth_use_case,
    users_crud_use_case,
    get_jwt_payload_jwt_bearer,
)
from presentation.schemas.auth import AuthSchema
from presentation.schemas.jwt import PayloadJWTSchema


def auth_form(
    username: str = Form(),
    password: str = Form(),
):
    return AuthSchema(username=username, password=password)


AuthForm = Annotated[AuthSchema, Depends(auth_form)]
JWTAuthUseCase = Annotated[AuthJWTUseCaseImpl, Depends(auth_use_case)]
UsersCrudUseCase = Annotated[UsersCrudUseCaseImpl, Depends(users_crud_use_case)]
PayloadJWTDependency = Annotated[PayloadJWTSchema, Depends(get_jwt_payload_jwt_bearer)]
