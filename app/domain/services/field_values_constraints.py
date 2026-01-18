from domain.contracts import ContractStringField
from domain.contracts.exc import ContractViolationError

from domain.contracts.require_schemas import ContractRequireSchema
from domain.users.business_rules import (
    PASSWORD_PATTERN,
    MIN_LEN_PASSWORD,
    MAX_LEN_PASSWORD,
    FORBIDDEN_NAMES,
)

from domain.utils import validate_string_by_pattern


def password_validator(value: str) -> bool:
    """
    Проверяет валидность устанавливаемого password.
    :param value: Строка password.
    :return: True or False.
    """

    if len(value) > 3 and (value.isalnum() or value.isalpha() or value.isnumeric()):
        return True
    return False
    raise InvalidValueToSetError("Недопустимый пароль.")
    return validate_string_by_pattern(value, PASSWORD_PATTERN, allow_empty=False)


class UserEntityValidators:
    @classmethod
    def password_validator(cls, password: str) -> bool:
        if len(password) > 3 and (
            password.isalnum() or password.isalpha() or password.isnumeric()
        ):
            return True
        return False

    @classmethod
    def check_type_password(cls, password: str) -> bool:
        return isinstance(password, str)


class UserEntityBusinessRules:
    """Класс для проверки бизнес-правил сущности пользователя."""

    contract_password = ContractStringField(
        field_name="password",
        nullable=False,
        min_length=MIN_LEN_PASSWORD,
        max_length=MAX_LEN_PASSWORD,
        requires=[
            ContractRequireSchema(
                handler=UserEntityValidators.check_type_password,
                contract="Пароль пользователя",
                violation=f"Должен быть строкой.",
            ),
            ContractRequireSchema(
                handler=UserEntityValidators.password_validator,
                contract="Пароль пользователя",
                violation=f"Должен быть не менее {MIN_LEN_PASSWORD} и не более {MAX_LEN_PASSWORD} символов.",
            ),
        ],
    )

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
        try:
            cls.contract_password(password)
        except ContractViolationError as e:
            raise ContractViolationBusinessRulesError(e)

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
        if not isinstance(username, str):
            raise ContractViolationBusinessRulesError("Недопустимый username.")
        if username in FORBIDDEN_NAMES:
            raise ContractViolationBusinessRulesError(
                f"Запрещено создавать пользователя с 'username'={username!r}."
            )
        if username == password:
            raise ContractViolationBusinessRulesError(
                "'username' и 'password' должны отличаться."
            )
        cls.check_password(password)
        return None
