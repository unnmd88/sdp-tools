from enum import StrEnum

from core.users.constants import MIN_ID, MAX_ID, MAX_LEN_PASSWORD, MIN_LEN_PASSWORD


class DomainRulesViolationsMessages(StrEnum):
    id_isinstance = "'id' должен быть числом"
    id_range = f"'id' должен быть числом в диапазоне от {MIN_ID} до {MAX_ID}."
    created_at_isinstance = "'created_at' должен быть типом 'datetime'"
    updated_at_isinstance = "'updated_at' должен быть типом 'datetime'"
    created_rule = "'created_at должен быть меньше updated_at'"
    updated_rule = "'updated_at должен быть больше created_at'"
    email = "'email' должен быть допустимым типом почтового ящика."
    password_type_must_be_bytes = 'Пароль должен быть последовательностью байтов.'
    password_length = (
        f'Пароль должен от {MIN_LEN_PASSWORD} до {MAX_LEN_PASSWORD} символов.'
    )
    bad_phone_number = 'Неверный формат номера телефона.'
    bad_telegram_username = 'Неверный формат @username для telegram-аккаунта.'
    description_must_be_lt_255 = "'Описание' должно быть не более 255 символов."


class BusinessRulesViolationsMessages(StrEnum):
    username = "'username' должен быть от 2 до 32 символов длиной и содержать только буквы латинского алфавита и цифры."
    firstname = (
        "'first_name' должен быть строкой и содержать только буквы латинского алфавита."
    )
    lastname = (
        "'last_name' должен быть строкой и содержать только буквы латинского алфавита."
    )
    firstname_and_lastname_must_be_different = (
        "'firstname' и 'lastname' должны быть разными."
    )
    username_and_password_must_be_different = (
        "username' и 'password' должны быть разными."
    )
    username_and_firstname_must_be_different = (
        "'username' и 'firstname' должны быть разными."
    )
    username_and_lastname_must_be_different = (
        "'username' и 'lastname' должны быть разными."
    )
