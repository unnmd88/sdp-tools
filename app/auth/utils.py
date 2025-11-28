import datetime
import random
import secrets
import string
from datetime import datetime as dt
from datetime import timedelta
from typing import AnyStr

import bcrypt
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


def hash_password(
    password: str,
) -> bytes:
    return bcrypt.hashpw(
        password.encode('utf-8'),
        bcrypt.gensalt(),
    )


def validate_password(
    password: str,
    hashed_password: bytes,
) -> bool:
    return bcrypt.checkpw(
        password=password.encode('utf-8'),
        hashed_password=hashed_password,
    )


def gen_password(
    min_length: int = settings.auth_jwt.passwd.min_length,
    max_length: int = settings.auth_jwt.passwd.max_length,
) -> str:
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(
        secrets.choice(chars) for _ in range(random.randint(min_length, max_length))
    )

