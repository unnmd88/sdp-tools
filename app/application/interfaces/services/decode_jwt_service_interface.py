from typing import Protocol, runtime_checkable

from application.dto.jwt_dto import AccessJWTPayloadDTO, RefreshJWTPayloadDTO
from domain.enums.unsorted import TokenTypesEnum


@runtime_checkable
class DecodeJWTServiceProtocol(Protocol):
    """Протокол для сервиса работы с JWT токенами"""

    def decode_jwt(self, token: str, expected_token_type: TokenTypesEnum) -> AccessJWTPayloadDTO | RefreshJWTPayloadDTO:
        """Декодировать и верифицировать токен"""
        ...

    def verify_token(self, token: str) -> bool:
        """Быстрая проверка валидности токена"""
        ...
