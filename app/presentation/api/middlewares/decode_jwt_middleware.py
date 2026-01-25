from collections.abc import Sequence, Awaitable, Coroutine, Callable

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import jwt
from typing import List, Optional
import time

from starlette import status

from application.services.exceptions import InvalidTokenTypeError, UnauthorizedError
from application.use_cases.users.decode_access_jwt_use_case import DecodeJWTUseCaseImpl


class JWTMiddleware(BaseHTTPMiddleware):
    """Middleware для проверки JWT токенов"""
    public_paths: Sequence[str] = (
        "/health",
        "/docs",
        "/openapi.json",
        "/refresh",
        "login",
        "auth",
    )
    def __init__(self, app, public_paths: Sequence[str] = None):
        super().__init__(app)

    async def dispatch(
        self,
        request: Request,
        call_next: Callable,
    ):
        #TODO: добавить кеширование
        if any(path in request.url.path for path in self.public_paths):
            return  await call_next(request)
        if (auth_header := request.headers.get("Authorization")) is None:
            print(f"auth_header: {auth_header}")
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Требуется авторизация"}
            )
        try:
            token_type, token = auth_header.split(" ")
        except Exception:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Требуется авторизация"}
            )
        if token_type != "Bearer":
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Требуется авторизация"}
            )
        if not token:
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"detail": "Требуется авторизация"}
            )
        use_case = DecodeJWTUseCaseImpl()
        try:
            request.state.user = use_case(access_token=token)
        except (InvalidTokenTypeError, UnauthorizedError) as e:
            return JSONResponse(
                status_code=e.status_code,
                content={"detail": e.message}
            )
            # raise HTTPException(
            #     status_code=e.status_code,
            #     detail=e.message,
            # )
            # return JSONResponse(
            #     status_code=401,
            #     content={"detail": "Требуется авторизация"}
            # )

        # Засекаем время выполнения
        start_time = time.perf_counter()
        response = await call_next(request)
        process_time = time.perf_counter() - start_time
        # Добавляем метаданные в заголовки
        response.headers["X-Process-Time"] = str(process_time)
        return response

    # def extract_token(self, request: Request) -> Optional[str]:
    #     # Из заголовка Authorization
    #     auth_header = request.headers.get("Authorization")
    #     if auth_header and auth_header.startswith("Bearer "):
    #         return auth_header[7:]  # Убираем "Bearer "
    #
    #     # Из query параметров
    #     token = request.query_params.get("token")
    #     if token:
    #         return token
    #
    #     # Из cookies
    #     token = request.cookies.get("access_token")
    #     if token:
    #         return token
    #
    #     return None



