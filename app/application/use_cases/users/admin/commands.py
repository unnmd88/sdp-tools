from dataclasses import dataclass, field
from typing import ClassVar

from domain.kernel.enums.keep_value_enum import Keep
from domain.kernel.enums.unsorted import Roles, Organizations


@dataclass(slots=True, kw_only=True, frozen=True)
class CreateUserCommand:
    operation_name: ClassVar[str] = "Создать  нового пользователя системы"
    customer_id: int

    firstname: str
    lastname: str
    username: str
    email: str | None
    organization: Organizations
    is_active: bool
    role: Roles
    phone_number: str | None
    telegram: str | None
    description: str
    password: str = field(repr=False)


@dataclass(slots=True, kw_only=True, frozen=True)
class UpdateUserByAdminCommand:
    operation_name: ClassVar[str] = "Обновить данные пользователя от администратора системы."
    customer_id: int
    subject_username: str

    firstname: str | Keep = Keep.VALUE
    lastname: str | Keep = Keep.VALUE
    username: str | Keep = Keep.VALUE
    email: str | None | Keep = Keep.VALUE
    organization: Organizations | Keep = Keep.VALUE
    is_active: bool | Keep = Keep.VALUE
    role: Roles | Keep = Keep.VALUE
    phone_number: str | None | Keep = Keep.VALUE
    telegram: str | None
    description: str


@dataclass(slots=True, kw_only=True, frozen=True)
class ResetUserPasswordByAdminCommand:
    """
    Сброс пароля пользователя администратором системы.
    Если пароль не указан(new_password=None), то будет сгенерирован случайный.
    """
    operation_name: ClassVar[str] = "Изменить пароль пользователя."
    customer_id: int
    subject_username: str

    new_password: str | None = field(repr=False)


@dataclass(slots=True, kw_only=True, frozen=True)
class DeleteUserCommand:
    """Удаление светофорного объекта"""
    operation_name: ClassVar[str] = "Удалить пользователя системы."

    customer_id: int
    subject_username: str