from collections.abc import MutableMapping
from typing import AnyStr

import jwt

from core.config import settings


def encode_jwt(
    payload: MutableMapping,
    private_key: str = settings.auth_jwt.private_key_path.read_text(encoding='utf-8'),
    algorithm: str = settings.auth_jwt.algorithm,
) -> str:
    encoded = jwt.encode(
        payload,
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