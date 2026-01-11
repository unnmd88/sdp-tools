def br_username_validator(value: str) -> bool:
    """
    Бизнес логика валидации username.

    Args:
        value(str): значение для валидации.

    Returns:
        bool: True если значение валидно, False - если нет.
    """
    return (
        2 < len(value) < 32
        and value.isalpha()
        or (value.isalnum() and not value.isnumeric())
    )


def br_first_name_or_lastname_validator(value: str) -> bool:
    """
    Бизнес логика валидации имени или фамилии.
    Args:
        value(str): значение для валидации.

    Returns:
        bool: True если значение валидно, False - если нет.

    """
    return 3 < len(value) < 16 and value.isalpha()
