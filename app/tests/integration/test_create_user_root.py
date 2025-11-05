import bcrypt
import pytest

from sqlalchemy.engine.result import Result
from sqlalchemy.sql.expression import select

from core.models import User
from core.models.database_api import DatabaseAPI
from users.create_root import create_root


@pytest.mark.asyncio(loop_scope='session')
async def test_create_user(t_dp_api: DatabaseAPI):
    async with t_dp_api.session_factory() as session:
        await create_root(session)

    async with t_dp_api.session_factory() as session:
        stmt = select(User).where(User.username == 'root')
        result: Result = await session.execute(stmt)
        usr_root = result.scalars().one()
        passwd_is_valid = bcrypt.checkpw(
            password='sdp2025'.encode('utf-8'),
            hashed_password=usr_root.password,
        )
        assert passwd_is_valid
