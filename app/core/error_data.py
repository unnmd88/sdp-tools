from core.http_codes import *

from enum import Enum
from typing import NamedTuple


class Error(NamedTuple):
    """Структурированное описание ошибки"""

    code: str
    message: str
    http_status_code: int


class ErrorData(Enum):
    """
    Полный перечень всех ошибок приложения.
    Используются пользовательские HTTP константы.
    """

    # ==================== ОБЩИЕ ОШИБКИ ====================
    INTERNAL_ERROR = Error(
        code="internal_error",
        message="Внутренняя ошибка сервера",
        http_status_code=HTTP_500_INTERNAL_SERVER_ERROR,
    )

    SERVICE_UNAVAILABLE = Error(
        code="service_unavailable",
        message="Сервис временно недоступен",
        http_status_code=HTTP_503_SERVICE_UNAVAILABLE,
    )

    TIMEOUT = Error(
        code="timeout",
        message="Превышено время ожидания",
        http_status_code=HTTP_504_GATEWAY_TIMEOUT,
    )

    CONFIGURATION_ERROR = Error(
        code="configuration_error",
        message="Ошибка конфигурации",
        http_status_code=HTTP_500_INTERNAL_SERVER_ERROR,
    )

    NOT_IMPLEMENTED = Error(
        code="not_implemented",
        message="Функционал не реализован",
        http_status_code=HTTP_501_NOT_IMPLEMENTED,
    )

    BAD_GATEWAY = Error(
        code="bad_gateway",
        message="Ошибка шлюза",
        http_status_code=HTTP_502_BAD_GATEWAY,
    )

    # ==================== ДОМЕННЫЕ ОШИБКИ ====================
    DOMAIN_ERROR = Error(
        code="domain_error",
        message="Ошибка бизнес-логики",
        http_status_code=HTTP_400_BAD_REQUEST,
    )

    ENTITY_NOT_FOUND = Error(
        code="entity_not_found",
        message="Сущность не найдена",
        http_status_code=HTTP_404_NOT_FOUND,
    )

    BUSINESS_RULE_VIOLATION = Error(
        code="business_rule_violation",
        message="Нарушение бизнес-правила",
        http_status_code=HTTP_422_UNPROCESSABLE_ENTITY,
    )

    DOMAIN_VALIDATION = Error(
        code="domain_validation",
        message="Ошибка валидации данных",
        http_status_code=HTTP_400_BAD_REQUEST,
    )

    DOMAIN_TYPE_VALIDATION = Error(
        code="domain_type_validation",
        message="Ошибка типа данных",
        http_status_code=HTTP_400_BAD_REQUEST,
    )

    DOMAIN_CONFLICT = Error(
        code="domain_conflict",
        message="Конфликт в бизнес-логике",
        http_status_code=HTTP_409_CONFLICT,
    )

    AGGREGATE_NOT_FOUND = Error(
        code="aggregate_not_found",
        message="Агрегат не найден",
        http_status_code=HTTP_404_NOT_FOUND,
    )

    VALUE_OBJECT_INVALID = Error(
        code="value_object_invalid",
        message="Невалидный объект-значение",
        http_status_code=HTTP_400_BAD_REQUEST,
    )

    ENTITY_ALREADY_EXISTS = Error(
        code="entity_already_exists",
        message="Сущность уже существует",
        http_status_code=HTTP_409_CONFLICT,
    )

    INVALID_STATE_TRANSITION = Error(
        code="invalid_state_transition",
        message="Некорректный переход состояния",
        http_status_code=HTTP_400_BAD_REQUEST,
    )

    # ==================== ПРИКЛАДНЫЕ ОШИБКИ ====================
    APPLICATION_ERROR = Error(
        code="application_error",
        message="Ошибка приложения",
        http_status_code=HTTP_400_BAD_REQUEST,
    )

    VALIDATION_ERROR = Error(
        code="validation_error",
        message="Ошибка валидации",
        http_status_code=HTTP_422_UNPROCESSABLE_ENTITY,
    )

    UNAUTHORIZED = Error(
        code="unauthorized",
        message="Не авторизован",
        http_status_code=HTTP_401_UNAUTHORIZED,
    )

    FORBIDDEN = Error(
        code="forbidden", message="Доступ запрещен", http_status_code=HTTP_403_FORBIDDEN
    )

    NOT_FOUND = Error(
        code="not_found",
        message="Ресурс не найден",
        http_status_code=HTTP_404_NOT_FOUND,
    )

    BAD_REQUEST = Error(
        code="bad_request",
        message="Некорректный запрос",
        http_status_code=HTTP_400_BAD_REQUEST,
    )

    CONFLICT = Error(
        code="conflict", message="Конфликт данных", http_status_code=HTTP_409_CONFLICT
    )

    RATE_LIMIT_EXCEEDED = Error(
        code="rate_limit_exceeded",
        message="Превышен лимит запросов",
        http_status_code=HTTP_429_TOO_MANY_REQUESTS,
    )

    PAYLOAD_TOO_LARGE = Error(
        code="payload_too_large",
        message="Слишком большой объем данных",
        http_status_code=HTTP_413_PAYLOAD_TOO_LARGE,
    )

    UNSUPPORTED_MEDIA_TYPE = Error(
        code="unsupported_media_type",
        message="Неподдерживаемый тип данных",
        http_status_code=HTTP_415_UNSUPPORTED_MEDIA_TYPE,
    )

    METHOD_NOT_ALLOWED = Error(
        code="method_not_allowed",
        message="Метод не разрешен",
        http_status_code=HTTP_405_METHOD_NOT_ALLOWED,
    )

    # ==================== ИНФРАСТРУКТУРНЫЕ ОШИБКИ ====================
    INFRASTRUCTURE_ERROR = Error(
        code="infrastructure_error",
        message="Ошибка инфраструктуры",
        http_status_code=HTTP_500_INTERNAL_SERVER_ERROR,
    )

    DATABASE_ERROR = Error(
        code="database_error",
        message="Ошибка базы данных",
        http_status_code=HTTP_500_INTERNAL_SERVER_ERROR,
    )

    REPOSITORY_ERROR = Error(
        code="repository_error",
        message="Ошибка репозитория",
        http_status_code=HTTP_500_INTERNAL_SERVER_ERROR,
    )

    EXTERNAL_SERVICE_ERROR = Error(
        code="external_service_error",
        message="Ошибка внешнего сервиса",
        http_status_code=HTTP_502_BAD_GATEWAY,
    )

    CACHE_ERROR = Error(
        code="cache_error",
        message="Ошибка кэша",
        http_status_code=HTTP_500_INTERNAL_SERVER_ERROR,
    )

    QUEUE_ERROR = Error(
        code="queue_error",
        message="Ошибка очереди",
        http_status_code=HTTP_500_INTERNAL_SERVER_ERROR,
    )

    STORAGE_ERROR = Error(
        code="storage_error",
        message="Ошибка хранилища",
        http_status_code=HTTP_500_INTERNAL_SERVER_ERROR,
    )

    NETWORK_ERROR = Error(
        code="network_error",
        message="Сетевая ошибка",
        http_status_code=HTTP_500_INTERNAL_SERVER_ERROR,
    )

    CONNECTION_ERROR = Error(
        code="connection_error",
        message="Ошибка соединения",
        http_status_code=HTTP_500_INTERNAL_SERVER_ERROR,
    )

    # ==================== API ОШИБКИ ====================
    API_ERROR = Error(
        code="api_error", message="Ошибка API", http_status_code=HTTP_400_BAD_REQUEST
    )

    INVALID_JSON = Error(
        code="invalid_json",
        message="Невалидный JSON",
        http_status_code=HTTP_400_BAD_REQUEST,
    )

    INVALID_CONTENT_TYPE = Error(
        code="invalid_content_type",
        message="Неверный Content-Type",
        http_status_code=HTTP_415_UNSUPPORTED_MEDIA_TYPE,
    )

    MISSING_REQUIRED_FIELD = Error(
        code="missing_required_field",
        message="Отсутствует обязательное поле",
        http_status_code=HTTP_400_BAD_REQUEST,
    )

    INVALID_PARAMETER = Error(
        code="invalid_parameter",
        message="Неверный параметр",
        http_status_code=HTTP_400_BAD_REQUEST,
    )

    # ==================== СЕРИАЛИЗАЦИЯ ====================
    SERIALIZATION_ERROR = Error(
        code="serialization_error",
        message="Ошибка сериализации",
        http_status_code=HTTP_500_INTERNAL_SERVER_ERROR,
    )

    DESERIALIZATION_ERROR = Error(
        code="deserialization_error",
        message="Ошибка десериализации",
        http_status_code=HTTP_400_BAD_REQUEST,
    )

    # ==================== АУТЕНТИФИКАЦИЯ И АВТОРИЗАЦИЯ ====================
    AUTHENTICATION_FAILED = Error(
        code="authentication_failed",
        message="Ошибка аутентификации",
        http_status_code=HTTP_401_UNAUTHORIZED,
    )

    INVALID_TOKEN = Error(
        code="invalid_token",
        message="Невалидный токен",
        http_status_code=HTTP_401_UNAUTHORIZED,
    )

    TOKEN_EXPIRED = Error(
        code="token_expired",
        message="Токен истек",
        http_status_code=HTTP_401_UNAUTHORIZED,
    )

    INVALID_CREDENTIALS = Error(
        code="invalid_credentials",
        message="Неверные учетные данные",
        http_status_code=HTTP_401_UNAUTHORIZED,
    )

    INSUFFICIENT_PERMISSIONS = Error(
        code="insufficient_permissions",
        message="Недостаточно прав",
        http_status_code=HTTP_403_FORBIDDEN,
    )

    ACCOUNT_DISABLED = Error(
        code="account_disabled",
        message="Аккаунт отключен",
        http_status_code=HTTP_403_FORBIDDEN,
    )

    ACCOUNT_LOCKED = Error(
        code="account_locked",
        message="Аккаунт заблокирован",
        http_status_code=HTTP_403_FORBIDDEN,
    )

    # ==================== ФАЙЛЫ И ЗАГРУЗКИ ====================
    FILE_NOT_FOUND = Error(
        code="file_not_found",
        message="Файл не найден",
        http_status_code=HTTP_404_NOT_FOUND,
    )

    FILE_TOO_LARGE = Error(
        code="file_too_large",
        message="Файл слишком большой",
        http_status_code=HTTP_413_PAYLOAD_TOO_LARGE,
    )

    INVALID_FILE_TYPE = Error(
        code="invalid_file_type",
        message="Недопустимый тип файла",
        http_status_code=HTTP_400_BAD_REQUEST,
    )

    UPLOAD_FAILED = Error(
        code="upload_failed",
        message="Ошибка загрузки файла",
        http_status_code=HTTP_500_INTERNAL_SERVER_ERROR,
    )

    # ==================== ПОЧТА И УВЕДОМЛЕНИЯ ====================
    EMAIL_ERROR = Error(
        code="email_error",
        message="Ошибка отправки email",
        http_status_code=HTTP_500_INTERNAL_SERVER_ERROR,
    )

    INVALID_EMAIL = Error(
        code="invalid_email",
        message="Неверный email адрес",
        http_status_code=HTTP_400_BAD_REQUEST,
    )

    NOTIFICATION_ERROR = Error(
        code="notification_error",
        message="Ошибка отправки уведомления",
        http_status_code=HTTP_500_INTERNAL_SERVER_ERROR,
    )

    # ==================== ВАЛИДАЦИЯ ДАННЫХ ====================
    INVALID_EMAIL_FORMAT = Error(
        code="invalid_email_format",
        message="Неверный формат email",
        http_status_code=HTTP_400_BAD_REQUEST,
    )

    INVALID_PHONE_FORMAT = Error(
        code="invalid_phone_format",
        message="Неверный формат телефона",
        http_status_code=HTTP_400_BAD_REQUEST,
    )

    INVALID_DATE_FORMAT = Error(
        code="invalid_date_format",
        message="Неверный формат даты",
        http_status_code=HTTP_400_BAD_REQUEST,
    )

    INVALID_URL_FORMAT = Error(
        code="invalid_url_format",
        message="Неверный формат URL",
        http_status_code=HTTP_400_BAD_REQUEST,
    )

    FIELD_TOO_SHORT = Error(
        code="field_too_short",
        message="Поле слишком короткое",
        http_status_code=HTTP_400_BAD_REQUEST,
    )

    FIELD_TOO_LONG = Error(
        code="field_too_long",
        message="Поле слишком длинное",
        http_status_code=HTTP_400_BAD_REQUEST,
    )

    REQUIRED_FIELD = Error(
        code="required_field",
        message="Обязательное поле",
        http_status_code=HTTP_400_BAD_REQUEST,
    )

    UNIQUE_CONSTRAINT = Error(
        code="unique_constraint",
        message="Значение должно быть уникальным",
        http_status_code=HTTP_409_CONFLICT,
    )

    # ==================== ПОЛЬЗОВАТЕЛЬСКИЕ ОШИБКИ ====================
    USER_NOT_FOUND = Error(
        code="user_not_found",
        message="Пользователь не найден",
        http_status_code=HTTP_404_NOT_FOUND,
    )

    USER_ALREADY_EXISTS = Error(
        code="user_already_exists",
        message="Пользователь уже существует",
        http_status_code=HTTP_409_CONFLICT,
    )

    INVALID_PASSWORD = Error(
        code="invalid_password",
        message="Неверный пароль",
        http_status_code=HTTP_400_BAD_REQUEST,
    )

    PASSWORD_TOO_WEAK = Error(
        code="password_too_weak",
        message="Слишком слабый пароль",
        http_status_code=HTTP_400_BAD_REQUEST,
    )

    PASSWORD_MISMATCH = Error(
        code="password_mismatch",
        message="Пароли не совпадают",
        http_status_code=HTTP_400_BAD_REQUEST,
    )

    # ==================== РАБОТА С ДАННЫМИ ====================
    DATA_INTEGRITY_ERROR = Error(
        code="data_integrity_error",
        message="Ошибка целостности данных",
        http_status_code=HTTP_500_INTERNAL_SERVER_ERROR,
    )

    DATA_VALIDATION_ERROR = Error(
        code="data_validation_error",
        message="Ошибка валидации данных",
        http_status_code=HTTP_400_BAD_REQUEST,
    )

    DATA_NOT_FOUND = Error(
        code="data_not_found",
        message="Данные не найдены",
        http_status_code=HTTP_404_NOT_FOUND,
    )

    DATA_ALREADY_EXISTS = Error(
        code="data_already_exists",
        message="Данные уже существуют",
        http_status_code=HTTP_409_CONFLICT,
    )

    # ==================== СИСТЕМНЫЕ ОШИБКИ ====================
    SYSTEM_ERROR = Error(
        code="system_error",
        message="Системная ошибка",
        http_status_code=HTTP_500_INTERNAL_SERVER_ERROR,
    )

    RESOURCE_BUSY = Error(
        code="resource_busy", message="Ресурс занят", http_status_code=HTTP_423_LOCKED
    )

    RESOURCE_LIMIT_EXCEEDED = Error(
        code="resource_limit_exceeded",
        message="Превышен лимит ресурсов",
        http_status_code=HTTP_429_TOO_MANY_REQUESTS,
    )

    # ==================== ВЕБ-СОКЕТЫ И REAL-TIME ====================
    WEBSOCKET_ERROR = Error(
        code="websocket_error",
        message="Ошибка WebSocket",
        http_status_code=HTTP_500_INTERNAL_SERVER_ERROR,
    )

    CONNECTION_LIMIT_EXCEEDED = Error(
        code="connection_limit_exceeded",
        message="Превышен лимит соединений",
        http_status_code=HTTP_429_TOO_MANY_REQUESTS,
    )

    # ==================== ПРОЧИЕ ОШИБКИ ====================
    OPERATION_NOT_ALLOWED = Error(
        code="operation_not_allowed",
        message="Операция не разрешена",
        http_status_code=HTTP_403_FORBIDDEN,
    )

    OPERATION_FAILED = Error(
        code="operation_failed",
        message="Операция не выполнена",
        http_status_code=HTTP_400_BAD_REQUEST,
    )

    OPERATION_TIMEOUT = Error(
        code="operation_timeout",
        message="Таймаут операции",
        http_status_code=HTTP_504_GATEWAY_TIMEOUT,
    )

    INVALID_OPERATION = Error(
        code="invalid_operation",
        message="Некорректная операция",
        http_status_code=HTTP_400_BAD_REQUEST,
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

    @property
    def http_status_code(self) -> int:
        """Возвращает HTTP статус код"""
        return self.value.http_status_code

    def __str__(self) -> str:
        """Строковое представление (код ошибки)"""
        return self.code

    # ==================== УТИЛИТНЫЕ МЕТОДЫ ====================
    @classmethod
    def from_code(cls, code: str) -> "ErrorData":
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
                "http_status_code": error.http_status_code,
                "enum_name": error.name,
            }
            for error in cls
        }


if __name__ == "__main__":
    e = ErrorData.INTERNAL_ERROR
    print(e.value)
