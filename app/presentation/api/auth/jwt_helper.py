import datetime
from datetime import timedelta, datetime as dt, timedelta as td
from typing import AnyStr

import jwt

from core.config import settings
from domain.dto.tokens import TokenDataDTO
from domain.enums.unsorted import TokenTypes, TokenFields
from domain.users.entities.user import UserEntity


class JWTHelper:
    @classmethod
    def encode_jwt(
        cls,
        payload: dict,
        private_key: str = settings.auth_jwt.private_key_path.read_text(
            encoding="utf-8"
        ),
        algorithm: str = settings.auth_jwt.algorithm,
        expire_timedelta: timedelta | None = None,
        expire_minutes: int = settings.auth_jwt.access_expire_minutes,
    ) -> str:
        now = dt.now(datetime.UTC)
        if expire_timedelta is not None:
            expire = now + expire_timedelta
        else:
            expire = now + timedelta(minutes=expire_minutes)
        return jwt.encode(
            {k: v for k, v in payload.items()} | {"exp": expire, "iat": now},
            private_key,
            algorithm,
        )

    @classmethod
    def decode_jwt(
        cls,
        token: AnyStr,
        public_key: str = settings.auth_jwt.public_key_path.read_text(encoding="utf-8"),
        algorithm: str = settings.auth_jwt.algorithm,
    ) -> dict[str, str]:
        return jwt.decode(
            jwt=token,
            key=public_key,
            algorithms=[algorithm],
        )

    @classmethod
    def _create_token(
        cls,
        token_type: TokenTypes,
        payload: dict[str, str],
        expire_minutes: int = settings.auth_jwt.access_expire_minutes,
        expire_timedelta: td | None = None,
    ) -> str:
        return cls.encode_jwt(
            payload=payload | {str(TokenFields.typ): token_type},
            expire_minutes=expire_minutes,
            expire_timedelta=expire_timedelta,
        )

    @classmethod
    def create_access_jwt(cls, user: UserEntity) -> str:
        payload = {
            str(TokenFields.user_id): user.id,
            str(TokenFields.sub): user.username,
            str(TokenFields.role): user.role,
            str(TokenFields.organization): user.organization,
            str(TokenFields.email): user.email,
        }
        return cls._create_token(
            token_type=TokenTypes.access,
            payload=payload,
            expire_minutes=settings.auth_jwt.access_expire_minutes,
        )

    @classmethod
    def create_refresh_jwt(cls, user: UserEntity) -> str:
        payload = {
            str(TokenFields.user_id): user.id,
            str(TokenFields.sub): user.username,
        }
        return cls._create_token(
            token_type=TokenTypes.refresh,
            payload=payload,
            expire_timedelta=td(days=settings.auth_jwt.refresh_expire_days),
        )

    @classmethod
    def issue_jwt(
        cls,
        user_entity: UserEntity,
        refresh_token: bool = False,
    ) -> TokenDataDTO:
        return TokenDataDTO(
            access_token=cls.create_access_jwt(user_entity),
            refresh_token=cls.create_refresh_jwt(user_entity)
            if refresh_token
            else None,
        )
