import asyncio

import pytest

from fastapi import HTTPException
from auth.token_validation import check_is_active_superuser
from tests.fixtures.fixtures_user import user_schemas


async def test_check_is_active_superuser(user_schemas):
    users = await asyncio.gather(*[check_is_active_superuser(u) for u in user_schemas])
    assert all(user.is_superuser for user in users)
    for user in users:
        user.is_superuser = False

    with pytest.raises(HTTPException):
        users = await asyncio.gather(*[check_is_active_superuser(u) for u in user_schemas])



