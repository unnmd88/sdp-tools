import bcrypt

from core.reg_exps import PASSWORD_PATTERN
from core.utils import checking_types, validate_string_by_pattern


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


@checking_types(isinstance_of=str, field_name_for_exception='password')
def check_password_to_set_is_valid(value: str) -> bool:
    """
    Проверяет валидность устанавливаемого password.
    :param value: Строка password.
    :return: True or False.
    """
    if len(value) > 3 and value.isalnum():
        return True
    return False
    return validate_string_by_pattern(value, PASSWORD_PATTERN, allow_empty=False)
