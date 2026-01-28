from typing import Protocol, runtime_checkable
from pathlib import Path
from datetime import datetime

from application.dto.jwt_dto import TokenDataDTO, AccessJWTPayloadDTO, RefreshJWTPayloadDTO
from application.dto.users import UserDTO
from domain.enums.unsorted import TokenTypesEnum


@runtime_checkable
class JWTServiceProtocol(Protocol):
    """Протокол для сервиса работы с JWT токенами"""

    # Основные публичные методы
    def issue_pair(self, user_dto: UserDTO) -> TokenDataDTO:
        """Выпустить пару access/refresh токенов"""
        ...

    def issue_access_jwt(self, user_dto: UserDTO) -> TokenDataDTO:
        """Выпустить только access токен"""
        ...

    def decode_jwt(self, token: str) -> AccessJWTPayloadDTO | RefreshJWTPayloadDTO:
        """Декодировать и верифицировать токен"""
        ...

    def verify_token(self, token: str) -> bool:
        """Быстрая проверка валидности токена"""
        ...

    # Дополнительные методы (опционально, но полезно для гибкости)
    def create_access_jwt(self, user_dto: UserDTO) -> str:
        """Создать access токен (raw string)"""
        ...

    def create_refresh_jwt(self, user_dto: UserDTO) -> str:
        """Создать refresh токен (raw string)"""
        ...

    def encode_jwt(
        self,
        *,
        user_dto: UserDTO,
        token_type: TokenTypesEnum
    ) -> str:
        """Низкоуровневое создание токена"""
        ...