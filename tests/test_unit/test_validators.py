import random

import pytest

from core.enums.entity import EntityIdRange
from core.field_validators import check_field_id_is_valid, check_field_email_is_valid


@pytest.mark.parametrize(
    '_id,expected',
    [
        (random.randint(EntityIdRange.MIN_ID, EntityIdRange.MAX_ID), True),
        (random.randint(EntityIdRange.MIN_ID, EntityIdRange.MAX_ID), True),
        (0, False),
        (3412414214, False),
        (-random.randint(EntityIdRange.MIN_ID, 9126731924872154), False),
    ]
)
def test_validate_id(_id, expected):
    """ Тест валидности id для объекта домена. """
    assert check_field_id_is_valid(_id) == expected


@pytest.mark.parametrize(
    'email,expected',
    [
        ('simple@mail.com', True),
        ('john_doe@example.io', True),
        ('john_doe', False),
        ('@', False),
        ('com', False),
    ]
)
def test_validate_email(email, expected):
    """ Тест валидности email для объекта домена. """
    assert check_field_email_is_valid(email) == expected