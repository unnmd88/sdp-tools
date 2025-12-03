import random
import string

import pytest

from core.enums import EntityIdRange


@pytest.fixture
def pk_id():
    return random.randint(EntityIdRange.MIN_ID, EntityIdRange.MAX_ID)


@pytest.fixture
def random_text():
    return random.choices(string.ascii_letters)
