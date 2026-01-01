from datetime import timedelta as td
from core.enums import TokenFields, TokenTypes
from core.users.entities.user import UserEntity
import datetime
from datetime import datetime as dt
from datetime import timedelta
from typing import AnyStr
import jwt
from core.config import settings


def encode_jwt(
    payload: dict,
    private_key: str = settings.auth_jwt.private_key_path.read_text(encoding='utf-8'),
    algorithm: str = settings.auth_jwt.algorithm,
    expire_timedelta: timedelta | None = None,
    expire_minutes: int = settings.auth_jwt.access_expire_minutes,
) -> str:
    now = dt.now(datetime.UTC)
    if expire_timedelta is not None:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    encoded = jwt.encode(
        {k: v for k, v in payload.items()} | {'exp': expire, 'iat': now},
        private_key,
        algorithm,
    )
    return encoded


def decode_jwt(
    token: AnyStr,
    public_key: str = settings.auth_jwt.public_key_path.read_text(encoding='utf-8'),
    algorithm: str = settings.auth_jwt.algorithm,
):
    decoded = jwt.decode(
        jwt=token,
        key=public_key,
        algorithms=[algorithm],
    )
    return decoded


def create_token(
    token_type: TokenTypes,
    payload: dict[str, str],
    expire_minutes: int = settings.auth_jwt.access_expire_minutes,
    expire_timedelta: td | None = None,
):
    return encode_jwt(
        payload=payload | {str(TokenFields.typ): token_type},
        expire_minutes=expire_minutes,
        expire_timedelta=expire_timedelta,
    )


def create_access_jwt(user: UserEntity):
    payload = {
        str(TokenFields.user_id): user.id,
        str(TokenFields.sub): user.username,
        str(TokenFields.role): user.role,
        str(TokenFields.organization): user.organization,
        str(TokenFields.email): user.email,
    }
    return create_token(
        token_type=TokenTypes.access,
        payload=payload,
        expire_minutes=settings.auth_jwt.access_expire_minutes,
    )


def create_refresh_jwt(user: UserEntity):
    payload = {
        str(TokenFields.user_id): user.id,
        str(TokenFields.sub): user.username,
    }
    return create_token(
        token_type=TokenTypes.refresh,
        payload=payload,
        expire_timedelta=td(days=settings.auth_jwt.refresh_expire_days),
    )


