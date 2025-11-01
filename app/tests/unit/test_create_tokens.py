from auth.create_tokens import create_access_jwt
from tests.fixtures.fixtures_user import user_schemas


def test_create_jwt(user_schemas):
    """
    Тестирует создание jwt.
    :param user_schemas: Схема данных сущности  User.
    :return: None
    """

    access_tokens = [create_access_jwt(u) for u in user_schemas]
    assert all(isinstance(u, str) for u in access_tokens)
    assert len(access_tokens) == len(set(access_tokens))  # Each token must be unique
    refresh_tokens = [create_access_jwt(u) for u in user_schemas]
    assert all(isinstance(u, str) for u in refresh_tokens)
    assert len(refresh_tokens) == len(set(refresh_tokens))  # Each token must be unique
