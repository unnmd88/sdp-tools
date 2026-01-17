import random
import secrets
import string

import bcrypt

from core.users.business_rules import MIN_LEN_PASSWORD, MAX_LEN_PASSWORD


class UserPasswordService:

    @classmethod
    def hash_password(cls, password: str) -> bytes:
        return bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt(),
        )

    @classmethod
    def verify_password(cls, password: str, hashed_password: bytes) -> bool:
        return bcrypt.checkpw(
            password=password.encode("utf-8"),
            hashed_password=hashed_password,
        )


    @classmethod
    def generate_password(cls) -> str:
        chars = string.ascii_letters + string.digits + string.punctuation
        return "".join(
            secrets.choice(chars) for _ in range(
                random.randint(MIN_LEN_PASSWORD, MAX_LEN_PASSWORD)
            )
        )


def hash_password(
    password: str,
) -> bytes:
    return bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt(),
    )


def validate_password(
    password: str,
    hashed_password: bytes,
) -> bool:
    return bcrypt.checkpw(
        password=password.encode("utf-8"),
        hashed_password=hashed_password,
    )


def gen_password(
    min_length: int = 3,
    max_length: int = 20,
) -> str:
    chars = string.ascii_letters + string.digits + string.punctuation
    return "".join(
        secrets.choice(chars) for _ in range(random.randint(min_length, max_length))
    )
