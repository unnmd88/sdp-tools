from core.exceptions.contract import ContractViolationBusinessRulesError
from core.users.constants import (
    MIN_LEN_FIRSTNAME,
    MAX_LEN_FIRSTNAME,
    MIN_LEN_LASTNAME,
    MAX_LEN_LASTNAME,
)
from core.users.rules_messages import BusinessRulesViolationsMessages


def br_username_validator(value: str) -> bool:
    """
    Бизнес правила для поля username сущности пользователя.

    Args:
        value(str): значение для валидации.
    Returns:
        bool: True если значение валидно.
    Raises:
        ContractViolationBusinessRulesError: если значение не валидно.
    """
    err_msg = None
    if not 2 < len(value) < 32:
        err_msg = f'{str(BusinessRulesViolationsMessages.username_length)}. Длина: {len(value)}'
    elif not value.isalnum() or value.isnumeric():
        err_msg = str(BusinessRulesViolationsMessages.username_contents)
    if err_msg:
        raise ContractViolationBusinessRulesError(f'{err_msg}. Значение={value}.')
    return True


def br_first_name_validator(value: str) -> bool:
    """
    Бизнес логика валидации фамилии lastname.
    Args:
        value(str): значение для валидации.

    Returns:
        bool: True если значение валидно, False - если нет.

    """
    err_msg = None
    if not MIN_LEN_LASTNAME < len(value) < MAX_LEN_LASTNAME:
        err_msg = f'{str(BusinessRulesViolationsMessages.firstname_length)}. Длина: {len(value)}'
    if not value.isalpha():
        err_msg = str(BusinessRulesViolationsMessages.firstname_contents)
    if err_msg:
        raise ContractViolationBusinessRulesError(f'{err_msg}. Значение={value}.')
    return True


def br_lastname_validator(value: str) -> bool:
    """
    Бизнес логика валидации имени firstname.
        Args:
            value(str): значение для валидации.

        Returns:
            bool: True если значение валидно, False - если нет.

        Raises:
            ContractViolationBusinessRulesError: если значение не валидно.

    """
    err_msg = None
    if not MIN_LEN_FIRSTNAME < len(value) < MAX_LEN_FIRSTNAME:
        err_msg = f'{str(BusinessRulesViolationsMessages.lastname_length)}. Длина: {len(value)}'
    if not value.isalpha():
        err_msg = str(BusinessRulesViolationsMessages.lastname_contents)
    if err_msg:
        raise ContractViolationBusinessRulesError(f'{err_msg}. Значение={value}.')
    return True
