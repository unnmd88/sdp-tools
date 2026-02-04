from core.http_codes import *

from enum import Enum, StrEnum
from typing import NamedTuple


class Error(NamedTuple):
    """Структурированное описание ошибки"""

    code: str
    private_message: str
    public_message: str = ""


class ErrorCodes(Enum):
    """
    Полный перечень всех ошибок приложения.
    Используются пользовательские HTTP константы.
    """

    # ==================== ОБЩИЕ ОШИБКИ ====================
    INTERNAL_ERROR = Error(
        code="internal_error",
        private_message="Внутренняя ошибка сервера",
        public_message="Ошибка запроса. Попробуйте позже.",
    )

    SERVICE_UNAVAILABLE = Error(
        code="service_unavailable",
        private_message="Сервис временно недоступен",
        public_message="Сервис временно недоступен",
    )

    TIMEOUT = Error(
        code="timeout",
        private_message="Превышено время ожидания",
        public_message="Превышено время ожидания",
    )


    # ==================== ДОМЕННЫЕ ОШИБКИ ====================
    DOMAIN_ERROR = Error(
        code="domain_error",
        private_message="Ошибка домена",
        public_message="Некорректный запрос.",
    )

    DOMAIN_CONTRACT_VIOLATION = Error(
        code="domain_contract_violation",
        private_message="Нарушение контракта домена",
        public_message="Некорректный запрос.",
    )

    ENTITY_NOT_FOUND = Error(
        code="entity_not_found",
        private_message="Сущность не найдена",
        public_message="Ресурс не найден",
    )

    DOMAIN_INVARIANT_VIOLATION = Error(
        code="domain_invariant_violation",
        private_message="Нарушение инварианта домена",
        public_message="Некорректный запрос.",
    )

    BUSINESS_RULE_VIOLATION = Error(
        code="business_rule_violation",
        private_message="Нарушение бизнес-правила",
        public_message="Некорректный запрос.",
    )

    DOMAIN_VALIDATION = Error(
        code="domain_validation",
        private_message="Ошибка валидации данных",
        public_message="Некорректный запрос.",
    )

    DOMAIN_TYPE_VALIDATION = Error(
        code="domain_type_validation",
        private_message="Ошибка типа данных",
        public_message="Некорректный запрос.",
    )

    ENTITY_ALREADY_EXISTS = Error(
        code="entity_already_exists",
        private_message="Сущность уже существует",
        public_message="Ресурс уже существует",
    )

    INVALID_STATE_TRANSITION = Error(
        code="invalid_state_transition",
        private_message="Некорректный переход состояния",
    )

    # ==================== ПРИКЛАДНЫЕ ОШИБКИ ====================
    APPLICATION_ERROR = Error(
        code="application_error",
        private_message="Ошибка приложения",
        public_message="Ошибка запроса. Попробуйте позже.",
    )

    VALIDATION_ERROR = Error(
        code="validation_error",
        private_message="Ошибка валидации",
        public_message="Некорректный запрос.",
    )

    INACTIVE_ACCOUNT = Error(
        code="inactive_account",
        private_message="Аккаунт не активен",
        public_message="Аккаунт не активен",
    )

    UNAUTHORIZED = Error(
        code="unauthorized",
        private_message="Не авторизован",
        public_message="Требуется вход в систему.",
    )


    FORBIDDEN = Error(
        code="forbidden",
        private_message="Доступ запрещен",
        public_message="Доступ запрещен",
    )

    PAYLOAD_TOO_LARGE = Error(
        code="payload_too_large",
        private_message="Слишком большой объем данных",
        public_message="Слишком большой объем данных",

    )

    UNSUPPORTED_MEDIA_TYPE = Error(
        code="unsupported_media_type",
        private_message="Неподдерживаемый тип данных",
        public_message="Неподдерживаемый тип данных",
    )

    REPOSITORY_CORRUPTED_ERROR = Error(
        code="repository_corrupted_error",
        private_message="Нарушение данных в репозитории",
        public_message="Сервис временно недоступен",
    )

    USER_CASE_ERROR = Error(
        code="use_case_error",
        private_message="Ошибка выполнения сценария",
        public_message="Ошибка запроса. Попробуйте позже.",
    )

    # ==================== ИНФРАСТРУКТУРНЫЕ ОШИБКИ ====================
    INFRASTRUCTURE_ERROR = Error(
        code="infrastructure_error",
        private_message="Ошибка инфраструктуры",
        public_message="Ошибка запроса. Попробуйте позже.",

    )

    TOKEN_ERROR = Error(
        code="token_error",
        private_message="Ошибка токена",
        public_message="Требуется вход в систему",
    )

    TOKEN_EXPIRED_ERROR = Error(
        code="rotten_token_error",
        private_message="Срок действия токена истек",
        public_message="Требуется вход в систему",
    )

    DATABASE_ERROR = Error(
        code="database_error",
        private_message="Ошибка базы данных",
        public_message="Ошибка запроса. Попробуйте позже.",
    )

    REPOSITORY_ERROR = Error(
        code="repository_error",
        private_message="Ошибка репозитория",
        public_message="Ошибка запроса. Попробуйте позже.",
    )

    REPOSITORY_UPDATE_ERROR = Error(
        code="repository_update_error",
        private_message="Ошибка обновления данных репозитория",
        public_message="Ошибка запроса. Попробуйте позже.",
    )

    CORRUPTED_DATA_ERROR = Error(
        code="corrupted_data_error",
        private_message="Данные невалидны или повреждены",
        public_message="Ошибка запроса. Попробуйте позже.",
    )

    CONNECTION_ERROR = Error(
        code="connection_error",
        private_message="Ошибка соединения",
        public_message="Сервис временно недоступен. Попробуйте позже.",
    )

    # ==================== API ОШИБКИ ====================

    INVALID_TOKEN_TYPE = Error(
        code="invalid_token_type",
        private_message="Неверный тип токена",
        public_message="Требуется вход в систему",
    )


    # ==================== АУТЕНТИФИКАЦИЯ И АВТОРИЗАЦИЯ ====================
    AUTHENTICATION_FAILED = Error(
        code="authentication_failed",
        private_message="Ошибка аутентификации",
        public_message="Неверный логин или пароль",
    )

    INSUFFICIENT_PERMISSIONS = Error(
        code="insufficient_permissions",
        private_message="Недостаточно прав",
        public_message="Недостаточно прав",
    )

    ACCOUNT_DISABLED = Error(
        code="account_disabled",
        private_message="Аккаунт отключен",
        public_message="Аккаунт отключен",
    )

    ACCOUNT_LOCKED = Error(
        code="account_locked",
        private_message="Аккаунт заблокирован",
        public_message="Аккаунт заблокирован",
    )

    # ==================== СИСТЕМНЫЕ ОШИБКИ ====================
    SYSTEM_ERROR = Error(
        code="system_error",
        private_message="Системная ошибка",
        public_message="Ошибка запроса. Попробуйте позже.",
    )


    # ==================== ВЕБ-СОКЕТЫ И REAL-TIME ====================
    WEBSOCKET_ERROR = Error(
        code="websocket_error",
        private_message="Ошибка WebSocket",
        public_message="Ошибка запроса. Попробуйте позже.",
    )

    CONNECTION_LIMIT_EXCEEDED = Error(
        code="connection_limit_exceeded",
        private_message="Превышен лимит соединений",
        public_message="Превышен лимит соединений",
    )

    # ==================== ПРОЧИЕ ОШИБКИ ====================
    OPERATION_NOT_ALLOWED = Error(
        code="operation_not_allowed",
        private_message="Операция не разрешена",
        public_message="Операция не разрешена",
    )


    # Property методы для удобного доступа
    @property
    def code(self) -> str:
        """Возвращает код ошибки"""
        return self.value.code

    @property
    def private_message(self) -> str:
        """Возвращает сообщение ошибки"""
        return self.value.private_message

    @property
    def public_message(self) -> str:
        """Возвращает сообщение ошибки"""
        return self.value.public_message

    def __str__(self) -> str:
        """Строковое представление (код ошибки)"""
        return self.code

    # ==================== УТИЛИТНЫЕ МЕТОДЫ ====================
    @classmethod
    def from_code(cls, code: str) -> "ErrorCodes":
        """Находит ErrorData по коду"""
        for error in cls:
            if error.code == code:
                return error
        raise ValueError(f"Неизвестный код ошибки: {code}")

    @classmethod
    def get_all_codes(cls) -> list[str]:
        """Возвращает список всех кодов ошибок"""
        return [error.code for error in cls]

    @classmethod
    def get_all_messages(cls) -> list[str]:
        """Возвращает список всех сообщений"""
        return [error.private_message for error in cls]

    @classmethod
    def to_dict(cls) -> dict:
        """Преобразует все ошибки в словарь"""
        return {
            error.code: {
                "message": error.private_message,
                "enum_name": error.name,
            }
            for error in cls
        }


if __name__ == "__main__":
    e = ErrorCodes.INTERNAL_ERROR
    print(e.value)
