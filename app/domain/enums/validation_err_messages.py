from enum import StrEnum

from domain.business_rules import (
    MIN_ID,
    MAX_ID,
    MIN_LEN_PASSWORD,
    MAX_LEN_PASSWORD,
)


class ErrorMessages(StrEnum):
    name_not_allowed = "Недопустимое имя {}: {}."
    value_str_length_range = "Недопустимое количество символов у поля {}={}. Должно быть в диапазоне от {} до {} символов"
    must_be_isalpha = "Поле {!r} должно содержать только буквы."
    must_be_valid_datetime = "Неверный формат даты/времени для {!r}: {}."
    cant_be_numeric = "Поле {!r} не может содержать только цифры: {}."
    cant_start_with_numeric = "Поле {!r} не может начинаться с цифры: {}."
    expected_type_string = "Для {!r} ожидается тип строка. Передано: {!r}."
    expected_type_positive_int = (
        "Для {} ожидается положительное целое число. Значение: {}."
    )
    expected_string_or_bytes = "Для {!r} ожидается строка или байты."
    expected_bool = "Для {!r} ожидается булево значение."
    password_can_not_be_empty = "Пароль не может быть пустым."

    invalid_enum_value = "Недопустимое значение для Enum-класса {}: {}."
    invalid_format = "Неверный формат {}: {}."

    must_be_from_to_chars = "{} Должно содержать от {} до {} символов."
    cannot_be_equal = "Значение {} не может быть совпадать с {}."

    id_isinstance = "'id' должен быть числом"
    id_range = f"'id' должен быть числом в диапазоне от {MIN_ID} до {MAX_ID}."
    created_at_isinstance = "'created_at' должен быть типом 'datetime'"
    updated_at_isinstance = "'updated_at' должен быть типом 'datetime'"
    created_rule = "'created_at должен быть меньше updated_at'"
    updated_rule = "'updated_at должен быть больше created_at'"
    email = "'email' должен быть допустимым типом почтового ящика."
    password_type_must_be_bytes = "Пароль должен быть последовательностью байтов."
    password_length = (
        f"Пароль должен от {MIN_LEN_PASSWORD} до {MAX_LEN_PASSWORD} символов."
    )
    bad_phone_number = "Неверный формат номера телефона."
    bad_telegram_username = "Неверный формат @username для telegram-аккаунта."
    description_must_be_lt_255 = "'Описание' должно быть не более 255 символов."

    user_not_found = "Пользователь с {}={} не найден."
    account_is_blocked = "Аккаунт пользователя с {}={} заблокирован."
    has_not_access = "У пользователя с {}={} нет прав доступа."

    invalid_token_type = "Неверный тип токена. Ожидается: {}."
    unknown_token_type = "Неизвестный тип токена: {}."

    invalid_username_or_password = "Неверное имя пользователя или пароль."
    inactive_user = "Пользователь неактивен."
    already_exists = "{} с {}={} уже существует."
    # username_length_range = value_str_length_range.format(
    #     MIN_LEN_USERNAME, MAX_LEN_USERNAME
    # )
    #
    # first_name_str_length_range = value_str_length_range.format(
    #     MIN_LEN_FIRSTNAME, MAX_LEN_FIRSTNAME
    # )
    #
    # lastname_length_range = value_str_length_range.format(
    #     MIN_LEN_LASTNAME, MAX_LEN_LASTNAME
    # )
