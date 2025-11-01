from collections.abc import Sequence

import pytest
from auth.create_tokens import create_access_jwt
from auth.schemas import UserSchema
from users.organizations import Organizations
from users.roles import Roles
from users.schemas import UserFromDbFullSchema


@pytest.fixture
def user_schemas() -> Sequence[UserSchema | UserFromDbFullSchema]:
    return [
        UserSchema(
            id=1,
            username='chook',
            email='chook@exapmle.com',
            is_active=True,
            is_admin=True,
            is_superuser=True,
            role=Roles.superuser,
            organization=Organizations.spetsdorproject,
        ),
        UserFromDbFullSchema(
            id=4,
            email='gekk@example.com',
            first_name='gekk',
            last_name='gekkov',
            username='iamgekk',
            organization=Organizations.spetsdorproject,
            password=b'ofshpsabdhf',
            is_active=True,
            is_admin=True,
            is_superuser=True,
            role=Roles.admin,
        ),
    ]


def test_create_jwt(user_schemas):
    """
    Тестирует создание jwt
    :param user_schemas:
    :return:
    """

    access_tokens = [create_access_jwt(u) for u in user_schemas]
    assert all(isinstance(u, str) for u in access_tokens)
    assert len(access_tokens) == len(set(access_tokens))  # Each token must be unique
    refresh_tokens = [create_access_jwt(u) for u in user_schemas]
    assert all(isinstance(u, str) for u in refresh_tokens)
    assert len(refresh_tokens) == len(set(refresh_tokens))  # Each token must be unique
