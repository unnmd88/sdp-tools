from dataclasses import dataclass, field
from typing import ClassVar

from domain.kernel.enums.keep_value_enum import Keep


@dataclass(slots=True, kw_only=True, frozen=True)
class UpdateUserCommand:
    operation_name: ClassVar[str] = "Обновить данные пользователя."
    customer_id: int
    subject_username: str

    firstname: str | Keep = Keep.VALUE
    lastname: str | Keep = Keep.VALUE
    username: str | Keep = Keep.VALUE
    email: str | None | Keep = Keep.VALUE
    phone_number: str | None | Keep = Keep.VALUE
    telegram: str | None | Keep = Keep.VALUE


@dataclass(slots=True, kw_only=True, frozen=True)
class ChangeUserPasswordCommand:
    """
    Изменить пароль пользователя.
    Если пароль не указан(new_password=None), то будет сгенерирован случайный.
    """
    operation_name: ClassVar[str] = "Изменить пароль пользователя."
    customer_id: int
    subject_username: str

    new_password: str | None = field(repr=False)