from enum import StrEnum

from core.users.business_rules import (
    MIN_ID,
    MAX_ID,
    MAX_LEN_PASSWORD,
    MIN_LEN_PASSWORD,
    MIN_LEN_USERNAME,
    MAX_LEN_USERNAME,
    MIN_LEN_FIRSTNAME,
    MAX_LEN_FIRSTNAME,
    MIN_LEN_LASTNAME,
    MAX_LEN_LASTNAME,
)


class DomainRulesViolationsMessages(StrEnum):
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


class BusinessRulesViolationsMessages(StrEnum):
    must_be_from_to_chars = "{} Должно содержать от {} до {} символов."

    err_username = "Ошибка поля 'username'."
    err_firstname = "Ошибка поля 'firstname'."
    err_lastname = "Ошибка поля 'lastname'."

    username_length = must_be_from_to_chars.format(
        str(err_username), MIN_LEN_USERNAME, MAX_LEN_USERNAME
    )
    username_contents = (
        "{} Должно содержать только буквы латинского алфавита или цифры от 0-9.".format(
            err_username
        )
    )

    firstname_length = must_be_from_to_chars.format(
        str(err_firstname), MIN_LEN_FIRSTNAME, MAX_LEN_FIRSTNAME
    )
    firstname_contents = "{} Должно содержать только буквы латинского алфавита.".format(
        err_firstname
    )

    lastname_length = must_be_from_to_chars.format(
        str(err_lastname), MIN_LEN_LASTNAME, MAX_LEN_LASTNAME
    )
    lastname_contents = "{} Должно содержать только буквы латинского алфавита.".format(
        err_lastname
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


if __name__ == "__main__":
    print(BusinessRulesViolationsMessages.username_length)
