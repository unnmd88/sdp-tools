from core.config import settings
from core.reg_exps import PASSWORD_PATTERN
from core.users.exceptions import InvalidValueToSetError
from core.users.user_security_polices import forbidden_patterns_in_username
from core.utils import checking_types, validate_string_by_pattern


@checking_types(isinstance_of=str, field_name_for_exception='password')
def check_password_to_set_constraints(value: str):
    """
    Проверяет валидность устанавливаемого password.
    :param value: Строка password.
    :return: True or False.
    """

    if len(value) > 3 and (value.isalnum() or value.isalpha() or value.isnumeric()):
        return None
    raise InvalidValueToSetError('Недопустимый пароль.')
    return validate_string_by_pattern(value, PASSWORD_PATTERN, allow_empty=False)


class UserEntityConstraints:
    """
    Класс, содержащий константы и ограничения для сущности пользователя системы(UserEntity).

    Этот класс определяет все бизнес-правила, ограничения длины и форматы данных,
    связанные с пользовательскими сущностями в системе.
    """

    @classmethod
    def check_password(cls, password: str) -> None:
        """
        Проверяет валидность имени пользователя и пароля по заданным критериям.

        Args:
            password (str): Пароль пользователя системы.

        Raises:
            InvalidValueToSetError: При недопустимом пароле пользователя.

        Returns:
            None: Если пароль допускается.
        """
        return check_password_to_set_constraints(password)
        
    @classmethod
    def check_username_and_password(
        cls,
        *,
        username: str,
        password: str,
    ) -> None:
        """
        Проверяет валидность имени пользователя и пароля по заданным критериям.

        Этот метод выполняет проверку корректности учетных данных,
        включая проверку длины, допустимых символов и требований к сложности пароля.

        Args:
            username (str): Имя пользователя системы.
            password (str): Пароль пользователя системы.

        Raises:
            InvalidValueToSetError: При недопустимом username и/или password.

        Returns:
            None: В случает успешной проверки username и password.
        """
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
