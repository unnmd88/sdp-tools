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
    _users: Result = await t_session.execute(select(User))
    assert _users.scalars().all() == user_models


# @pytest.mark.asyncio(loop_scope="session")
# async def test_create_user(t_session: AsyncSession):
#     new_user = User(
#         first_name='chook',
#         last_name='gekk',
#         organization='SDP',
#         username='chook@gekk',
#         password=b'password1',
#         is_active=True,
#         is_admin=True,
#         is_superuser=True,
#         role='superman',
#     )

#     t_session.add(new_user)
#     await t_session.commit()
#     # await t_session.refresh(new_user)
