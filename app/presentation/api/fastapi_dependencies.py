from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.params import Form
from dishka.integrations.fastapi import FromDishka

from infrastructure.auth.jwt.jwt_service import DecodeJWTService
from application.dtos.jwt_dto import AccessJWTPayloadDTO, RefreshJWTPayloadDTO
from core.config import settings
from infrastructure.auth.jwt.rules import DecodeJWTSettings
from presentation.schemas.auth import AuthSchema

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=settings.login_url,
)


def auth_form(
    username: str = Form(),
    password: str = Form(),
):
    return AuthSchema(username=username, password=password)


AuthFormDep = Annotated[AuthSchema, Depends(auth_form)]


def _get_decode_jwt_service() -> DecodeJWTService:
    """Фабрика для создания DecodeJWTService"""
    decode_settings = DecodeJWTSettings()
    return DecodeJWTService(
        public_key=decode_settings.public_key_path.resolve().read_text("utf-8"),
        algorithm=decode_settings.algorithm,
    )


async def get_access_token_payload(
    token: Annotated[str, Depends(oauth2_scheme)],
) -> AccessJWTPayloadDTO:
    """
    Зависимость для получения декодированного access токена.
    Вся валидация и проверка типа токена происходит в DecodeJWTService.
    """
    decode_jwt_service = _get_decode_jwt_service()
    return decode_jwt_service.decode_access_jwt(token)


async def get_refresh_token_payload(
    refresh_token: Annotated[str, Depends(oauth2_scheme)],
) -> RefreshJWTPayloadDTO:
    """Зависимость для получения декодированного refresh токена из тела запроса"""
    decode_jwt_service = _get_decode_jwt_service()
    return decode_jwt_service.decode_refresh_jwt(refresh_token)


AccessTokenDep = Annotated[AccessJWTPayloadDTO, Depends(get_access_token_payload)]
RefreshTokenDep = Annotated[RefreshJWTPayloadDTO, Depends(get_refresh_token_payload)]


# async def get_user_id_from_access_token(
#     token_dto: AccessTokenDep,
# ) -> int:
#     """Зависимость для получения только user_id из access токена"""
#     return token_dto.user_id
#
# async def get_user_id_from_refresh_token(
#     token_dto: RefreshTokenDep,
# ) -> int:
#     """Зависимость для получения только user_id из refresh токена"""
#     return token_dto.user_id
