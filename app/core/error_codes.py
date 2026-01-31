from core.http_codes import *

from enum import Enum, StrEnum
from typing import NamedTuple


class Error(NamedTuple):
    """Структурированное описание ошибки"""

    code: str
    message: str


class ErrorCodes(Enum):
    """
    Полный перечень всех ошибок приложения.
    Используются пользовательские HTTP константы.
    """

    # ==================== ОБЩИЕ ОШИБКИ ====================
    INTERNAL_ERROR = Error(
        code="internal_error",
        message="Внутренняя ошибка сервера",
    )

    SERVICE_UNAVAILABLE = Error(
        code="service_unavailable",
        message="Сервис временно недоступен",
    )

    TIMEOUT = Error(
        code="timeout",
        message="Превышено время ожидания",
    )

    CONFIGURATION_ERROR = Error(
        code="configuration_error",
        message="Ошибка конфигурации",
    )

    NOT_IMPLEMENTED = Error(
        code="not_implemented",
        message="Функционал не реализован",
    )

    BAD_GATEWAY = Error(
        code="bad_gateway",
        message="Ошибка шлюза",
    )

    # ==================== ДОМЕННЫЕ ОШИБКИ ====================
    DOMAIN_ERROR = Error(
        code="domain_error",
        message="Ошибка бизнес-логики",
    )

    DOMAIN_CONTRACT_VIOLATION = Error(
        code="domain_contract_violation",
        message="Нарушение контракта домена",
    )

    ENTITY_NOT_FOUND = Error(
        code="entity_not_found",
        message="Сущность не найдена",
    )

    DOMAIN_INVARIANT_VIOLATION = Error(
        code="domain_invariant_violation",
        message="Нарушение инварианта домена",
    )

    BUSINESS_RULE_VIOLATION = Error(
        code="business_rule_violation",
        message="Нарушение бизнес-правила",
    )

    DOMAIN_VALIDATION = Error(
        code="domain_validation",
        message="Ошибка валидации данных",
    )

    DOMAIN_TYPE_VALIDATION = Error(
        code="domain_type_validation",
        message="Ошибка типа данных",
    )

    DOMAIN_CONFLICT = Error(
        code="domain_conflict",
        message="Конфликт в бизнес-логике",
    )

    AGGREGATE_NOT_FOUND = Error(
        code="aggregate_not_found",
        message="Агрегат не найден",
    )

    VALUE_OBJECT_INVALID = Error(
        code="value_object_invalid",
        message="Невалидный объект-значение",
    )

    ENTITY_ALREADY_EXISTS = Error(
        code="entity_already_exists",
        message="Сущность уже существует",
    )

    INVALID_STATE_TRANSITION = Error(
        code="invalid_state_transition",
        message="Некорректный переход состояния",
    )

    # ==================== ПРИКЛАДНЫЕ ОШИБКИ ====================
    APPLICATION_ERROR = Error(
        code="application_error",
        message="Ошибка приложения",
    )

    VALIDATION_ERROR = Error(
        code="validation_error",
        message="Ошибка валидации",
    )

    INACTIVE_ACCOUNT = Error(
        code="inactive_account",
        message="Аккаунт не активен",
    )

    UNAUTHORIZED = Error(
        code="unauthorized",
        message="Не авторизован",
    )

    FORBIDDEN = Error(
        code="forbidden",
        message="Доступ запрещен",
    )

    NOT_FOUND = Error(
        code="not_found",
        message="Ресурс не найден",
    )

    BAD_REQUEST = Error(
        code="bad_request",
        message="Некорректный запрос",
    )

    CONFLICT = Error(
        code="conflict",
        message="Конфликт данных",
    )

    RATE_LIMIT_EXCEEDED = Error(
        code="rate_limit_exceeded",
        message="Превышен лимит запросов",
    )

    PAYLOAD_TOO_LARGE = Error(
        code="payload_too_large",
        message="Слишком большой объем данных",
    )

    UNSUPPORTED_MEDIA_TYPE = Error(
        code="unsupported_media_type",
        message="Неподдерживаемый тип данных",
    )

    METHOD_NOT_ALLOWED = Error(
        code="method_not_allowed",
        message="Метод не разрешен",
    )

    USER_CASE_ERROR = Error(
        code="use_case_error",
        message="Ошибка выполнения сценария",
    )

    # ==================== ИНФРАСТРУКТУРНЫЕ ОШИБКИ ====================
    INFRASTRUCTURE_ERROR = Error(
        code="infrastructure_error",
        message="Ошибка инфраструктуры",
    )

    TOKEN_ERROR = Error(
        code="token_error",
        message="Ошибка токена",
    )

    ROTTEN_TOKEN_ERROR = Error(
        code="rotten_token_error",
        message="Срок действия токена истек",
    )

    DATABASE_ERROR = Error(
        code="database_error",
        message="Ошибка базы данных",
    )

    REPOSITORY_ERROR = Error(
        code="repository_error",
        message="Ошибка репозитория",
    )

    EXTERNAL_SERVICE_ERROR = Error(
        code="external_service_error",
        message="Ошибка внешнего сервиса",
    )

    CACHE_ERROR = Error(
        code="cache_error",
        message="Ошибка кэша",
    )

    QUEUE_ERROR = Error(
        code="queue_error",
        message="Ошибка очереди",
    )

    STORAGE_ERROR = Error(
        code="storage_error",
        message="Ошибка хранилища",
    )

    NETWORK_ERROR = Error(
        code="network_error",
        message="Сетевая ошибка",
    )

    CONNECTION_ERROR = Error(
        code="connection_error",
        message="Ошибка соединения",
    )

    # ==================== API ОШИБКИ ====================
    API_ERROR = Error(
        code="api_error",
        message="Ошибка API",
    )

    INVALID_JSON = Error(
        code="invalid_json",
        message="Невалидный JSON",
    )

    INVALID_TOKEN_TYPE = Error(
        code="invalid_token_type",
        message="Неверный тип токена",
    )

    INVALID_CONTENT_TYPE = Error(
        code="invalid_content_type",
        message="Неверный Content-Type",
    )

    MISSING_REQUIRED_FIELD = Error(
        code="missing_required_field",
        message="Отсутствует обязательное поле",
    )

    INVALID_PARAMETER = Error(
        code="invalid_parameter",
        message="Неверный параметр",
    )

    # ==================== СЕРИАЛИЗАЦИЯ ====================
    SERIALIZATION_ERROR = Error(
        code="serialization_error",
        message="Ошибка сериализации",
    )

    DESERIALIZATION_ERROR = Error(
        code="deserialization_error",
        message="Ошибка десериализации",
    )

    # ==================== АУТЕНТИФИКАЦИЯ И АВТОРИЗАЦИЯ ====================
    AUTHENTICATION_FAILED = Error(
        code="authentication_failed",
        message="Ошибка аутентификации",
    )

    INVALID_TOKEN = Error(
        code="invalid_token",
        message="Невалидный токен",
    )

    TOKEN_EXPIRED = Error(
        code="token_expired",
        message="Токен истек",
    )

    INVALID_CREDENTIALS = Error(
        code="invalid_credentials",
        message="Неверные учетные данные",
    )

    INSUFFICIENT_PERMISSIONS = Error(
        code="insufficient_permissions",
        message="Недостаточно прав",
    )

    ACCOUNT_DISABLED = Error(
        code="account_disabled",
        message="Аккаунт отключен",
    )

    ACCOUNT_LOCKED = Error(
        code="account_locked",
        message="Аккаунт заблокирован",
    )

    # ==================== ФАЙЛЫ И ЗАГРУЗКИ ====================
    FILE_NOT_FOUND = Error(
        code="file_not_found",
        message="Файл не найден",
    )

    FILE_TOO_LARGE = Error(
        code="file_too_large",
        message="Файл слишком большой",
    )

    INVALID_FILE_TYPE = Error(
        code="invalid_file_type",
        message="Недопустимый тип файла",
    )

    UPLOAD_FAILED = Error(
        code="upload_failed",
        message="Ошибка загрузки файла",
    )

    # ==================== ПОЧТА И УВЕДОМЛЕНИЯ ====================
    EMAIL_ERROR = Error(
        code="email_error",
        message="Ошибка отправки email",
    )

    INVALID_EMAIL = Error(
        code="invalid_email",
        message="Неверный email адрес",
    )

    NOTIFICATION_ERROR = Error(
        code="notification_error",
        message="Ошибка отправки уведомления",
    )

    # ==================== ВАЛИДАЦИЯ ДАННЫХ ====================
    INVALID_EMAIL_FORMAT = Error(
        code="invalid_email_format",
        message="Неверный формат email",
    )

    INVALID_PHONE_FORMAT = Error(
        code="invalid_phone_format",
        message="Неверный формат телефона",
    )

    INVALID_DATE_FORMAT = Error(
        code="invalid_date_format",
        message="Неверный формат даты",
    )

    INVALID_URL_FORMAT = Error(
        code="invalid_url_format",
        message="Неверный формат URL",
    )

    FIELD_TOO_SHORT = Error(
        code="field_too_short",
        message="Поле слишком короткое",
    )

    FIELD_TOO_LONG = Error(
        code="field_too_long",
        message="Поле слишком длинное",
    )

    REQUIRED_FIELD = Error(
        code="required_field",
        message="Обязательное поле",
    )

    UNIQUE_CONSTRAINT = Error(
        code="unique_constraint",
        message="Значение должно быть уникальным",
    )

    # ==================== ПОЛЬЗОВАТЕЛЬСКИЕ ОШИБКИ ====================
    USER_NOT_FOUND = Error(
        code="user_not_found",
        message="Пользователь не найден",
    )

    USER_ALREADY_EXISTS = Error(
        code="user_already_exists",
        message="Пользователь уже существует",
    )

    INVALID_PASSWORD = Error(
        code="invalid_password",
        message="Неверный пароль",
    )

    PASSWORD_TOO_WEAK = Error(
        code="password_too_weak",
        message="Слишком слабый пароль",
    )

    PASSWORD_MISMATCH = Error(
        code="password_mismatch",
        message="Пароли не совпадают",
    )

    # ==================== РАБОТА С ДАННЫМИ ====================
    DATA_INTEGRITY_ERROR = Error(
        code="data_integrity_error",
        message="Ошибка целостности данных",
    )

    DATA_VALIDATION_ERROR = Error(
        code="data_validation_error",
        message="Ошибка валидации данных",
    )

    DATA_NOT_FOUND = Error(
        code="data_not_found",
        message="Данные не найдены",
    )

    DATA_ALREADY_EXISTS = Error(
        code="data_already_exists",
        message="Данные уже существуют",
    )

    # ==================== СИСТЕМНЫЕ ОШИБКИ ====================
    SYSTEM_ERROR = Error(
        code="system_error",
        message="Системная ошибка",
    )

    RESOURCE_BUSY = Error(
        code="resource_busy",
        message="Ресурс занят",
    )

    RESOURCE_LIMIT_EXCEEDED = Error(
        code="resource_limit_exceeded",
        message="Превышен лимит ресурсов",
    )

    # ==================== ВЕБ-СОКЕТЫ И REAL-TIME ====================
    WEBSOCKET_ERROR = Error(
        code="websocket_error",
        message="Ошибка WebSocket",
    )

    CONNECTION_LIMIT_EXCEEDED = Error(
        code="connection_limit_exceeded",
        message="Превышен лимит соединений",
    )

    # ==================== ПРОЧИЕ ОШИБКИ ====================
    OPERATION_NOT_ALLOWED = Error(
        code="operation_not_allowed",
        message="Операция не разрешена",
    )

    OPERATION_FAILED = Error(
        code="operation_failed",
        message="Операция не выполнена",
    )

    OPERATION_TIMEOUT = Error(
        code="operation_timeout",
        message="Таймаут операции",
    )

    INVALID_OPERATION = Error(
        code="invalid_operation",
        message="Некорректная операция",
    )

    # Property методы для удобного доступа
    @property
    def code(self) -> str:
        """Возвращает код ошибки"""
        return self.value.code

    @property
    def message(self) -> str:
        """Возвращает сообщение ошибки"""
        return self.value.message


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
        return [error.message for error in cls]

    @classmethod
    def to_dict(cls) -> dict:
        """Преобразует все ошибки в словарь"""
        return {
            error.code: {
                "message": error.message,
                "enum_name": error.name,
            }
            for error in cls
        }


if __name__ == "__main__":
    e = ErrorCodes.INTERNAL_ERROR
    print(e.value)
