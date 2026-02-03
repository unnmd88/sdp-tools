import time
from collections.abc import Callable
from typing import Any

from fastapi import Request, HTTPException
from fastapi.routing import APIRoute
from fastapi.security import OAuth2PasswordBearer
from starlette import status
from application.use_cases.users.get_user_from_repo_by_jwt_use_case import (
    GetUserFromRepoByJWTUseCaseImpl,
)
from application.use_cases.users.get_user_use_case import GetUserUseCaseImpl
from infrastructure.database.api import db_api
from infrastructure.database.user_reposirory import UsersSqlAlchemyRepository
from presentation.api.dependencies.di import oauth2_scheme
from utils.extract_token import extract_token


class JWTUserAPIRoute(APIRoute):
    """
    APIRoute, который автоматически добавляет пользователя в Request
    на основе JWT токена.
    """

    def __init__(
        self,
        path: str,
        endpoint: Callable,
        *,
        active_user_require: bool = True,
        **kwargs,
    ):
        self.active_user_require = active_user_require
        super().__init__(path, endpoint, **kwargs)

    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Any:
            token = extract_token(request.headers.get("Authorization"))
            if not hasattr(request.state, "start_time"):
                request.state.start_time = time.perf_counter()
            async with db_api.session_factory() as session:
                print(f"2222222  {self.active_user_require=}")
                get_active_user_from_repo_use_case = GetUserFromRepoByJWTUseCaseImpl(
                    get_user_use_case=GetUserUseCaseImpl(
                        user_repository=UsersSqlAlchemyRepository(session=session)
                    ),
                    decode_service=DecodeAccessJWTService(),
                    require_active_user=self.active_user_require,
                )
                try:
                    request.state.user = await get_active_user_from_repo_use_case(token)
                except (DomainInactiveUserError, DomainEntityNotFoundError) as e:
                    raise HTTPException(
                        status_code=e.http_status,
                        detail=e._private_message,
                    )
            response = await original_route_handler(request)

            if hasattr(request.state, "start_time"):
                response.headers["X-Process-Time"] = str(
                    time.perf_counter() - request.state.start_time
                )

            if hasattr(request.state, "is_authenticated"):
                response.headers["X-Authenticated"] = str(
                    request.state.is_authenticated
                )
            return response

        return custom_route_handler


def jwt_route_class_factory(
    *,
    active_user_require: bool = True,
):
    """
    Создает класс JWTUserAPIRoute с заданными параметрами
    """

    class DynamicJWTUserAPIRoute(JWTUserAPIRoute):
        def __init__(
            self,
            path: str,
            endpoint: Callable,
            **kwargs,
        ):
            super().__init__(
                path, endpoint, active_user_require=active_user_require, **kwargs
            )

    return DynamicJWTUserAPIRoute
