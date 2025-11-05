import pytest

from sqlalchemy.engine.result import Result
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.sql.expression import select

from core.models import User
from tests.integration.conftest import user_models


@pytest.mark.asyncio(loop_scope='session')
async def test_create_user(t_session: AsyncSession, user_models):
    t_session.add_all(user_models)
    await t_session.commit()

    stmt = select(User).where(User.username.in_([model.username for model in user_models]))

    _users: Result = await t_session.execute(stmt)
    assert _users.scalars().all() == user_models



