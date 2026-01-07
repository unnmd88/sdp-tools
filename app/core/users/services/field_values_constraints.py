from core.config import settings
from core.reg_exps import PASSWORD_PATTERN
from core.users.exceptions import InvalidValueToSetError
from core.utils import checking_types, validate_string_by_pattern

forbidden_patterns_in_username: frozenset[str] = frozenset(
    (
        'root',
    )
)


@checking_types(isinstance_of=str, field_name_for_exception='password')
def check_password_to_set_constraints(value: str):
    """
    Проверяет валидность устанавливаемого password.
    :param value: Строка password.
    :return: True or False.
    """

    if len(value) > 3 and value.isalnum():
        return None
    raise InvalidValueToSetError('Недопустимый пароль.')
    return validate_string_by_pattern(value, PASSWORD_PATTERN, allow_empty=False)


class UserEntityConstraints:

    @classmethod
    def check_password(cls, password: str) -> None:
        return check_password_to_set_constraints(password)
        
    @classmethod
    def check_username_and_password(
        cls,
        *,
        username: str,
        password: str = None,
    ) -> None:
        if username == settings.default_superuser_creds.name:
            raise InvalidValueToSetError(
                f"Ошибка: запрещено создавать пользователя "
                f"с 'username'={settings.default_superuser_creds.name!r} "
                f"через данный интерфейс."
            )
        for pattern in forbidden_patterns_in_username:
            if pattern in username:
                field_name = 'username'
            elif pattern in password:
                field_name = 'пароле'
            else:
                field_name = None
            if field_name:
                raise InvalidValueToSetError(
                    f'Ошибка: запрещено создавать пользователя с фрагментом {pattern!r} в {field_name!r}.'
                )
        if username == password:
            raise InvalidValueToSetError('Ошибка: username и пароль должны отличаться')
        cls.check_password(password)
        return None
    

@checking_types(isinstance_of=str, field_name_for_exception='password')
def check_password_to_set_constraints(value: str) -> bool:
    """
    Проверяет валидность устанавливаемого password.
    :param value: Строка password.
    :return: True or False.
    """
    if len(value) > 3 and value.isalnum():
        return True
    return False
    return validate_string_by_pattern(value, PASSWORD_PATTERN, allow_empty=False)
