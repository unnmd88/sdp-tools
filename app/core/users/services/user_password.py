import random
import secrets
import string

import bcrypt


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
    min_length: int = 3,
    max_length: int = 20,
) -> str:
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(
        secrets.choice(chars) for _ in range(random.randint(min_length, max_length))
    )
