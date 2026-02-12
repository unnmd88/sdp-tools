from enum import StrEnum


class ContextKey(StrEnum):
    """Единый источник правды для всех ключей контекста."""

    # Сущности
    ENTITY_NAME = "entity_name"
    ENTITY_ID = "entity_id"
    ENTITY_TYPE = "entity_type"

    # Валидация
    FIELD = "field"
    VALUE = "value"
    VALIDATOR = "validator"
    RULE = "rule"
    EXPECTED = "expected"
    EXPECTED_PATTERN = "expected_pattern"

    # Бизнес-правила
    AGGREGATE_NAME = "aggregate_name"
    AGGREGATE_ID = "aggregate_id"
    BUSINESS_RULE = "business_rule"

    # Технические
    REQUEST_ID = "request_id"
    TIMESTAMP = "timestamp"
    REPOSITORY = "repository"

    # Ошибки
    ERROR_CODE = "error_code"
    VIOLATION = "violation"