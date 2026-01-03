import random
import secrets
import string

import bcrypt

from core.reg_exps import PASSWORD_PATTERN
from core.utils import checking_simple_types, validate_string_by_pattern


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


@checking_simple_types(type_to_check=str, field_name='password')
def check_password_to_set_is_valid(value: str) -> bool:
    """
    Проверяет валидность устанавливаемого password.
    :param value: Строка password.
    :return: True or False.
    """
    return validate_string_by_pattern(value, PASSWORD_PATTERN, allow_empty=False)
