from auth.token_validation import check_is_active_superuser
from tests.fixtures.fixtures_user import user_schemas
import pytest


# @pytest.mark.asyncio
async def test_check_is_active_superuser(user_schemas):
    for user in user_schemas:
        assert await check_is_active_superuser(user)
    # assert all(await check_is_active_superuser(u) for u in user_schemas)


