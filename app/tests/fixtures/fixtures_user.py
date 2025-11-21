from collections.abc import Sequence

import pytest
from auth.schemas import UserSchema
from users.organizations import Organizations
from users.roles import Roles
from users.schemas import UserFromDbFullSchema


@pytest.fixture
def user_schemas() -> Sequence[UserSchema | UserFromDbFullSchema]:
    """
    Формирует последовательность схем.
    :return: Последовательность схем юзера.
    """
    return [
        UserSchema(
            id=1,
            username='chook',
            email='chook@exapmle.com',
            is_active=True,
            is_admin=True,
            is_superuser=True,
            role=Roles.superuser,
            organization=Organizations.SDP,
        ),
        UserFromDbFullSchema(
            id=4,
            email='gekk@example.com',
            first_name='gekk',
            last_name='gekkov',
            username='iamgekk',
            organization=Organizations.SDP,
            password=b'ofshpsabdhf',
            is_active=True,
            is_admin=True,
            is_superuser=True,
            role=Roles.admin,
        ),
    ]
