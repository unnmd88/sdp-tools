import bcrypt
import pytest

from sqlalchemy.engine.result import Result
from sqlalchemy.sql.expression import select

from core.models import User
from core.database.api import DatabaseAPI
from users.create_root import create_root


@pytest.mark.asyncio(loop_scope='session')
async def test_create_user_root(t_dp_api: DatabaseAPI):

    async with t_dp_api.session_factory() as sess:
        user_root1: User = await create_root(sess)

    async with t_dp_api.session_factory() as sess:
        stmt = select(User).where(User.username == 'root')
        result: Result = await sess.execute(stmt)
        usr_root2 = result.scalars().one()
        passwd_is_valid = bcrypt.checkpw(
            password='sdp2025'.encode('utf-8'),
            hashed_password=usr_root2.password,
        )
        assert isinstance(user_root1, User) and isinstance(usr_root2, User)
        assert isinstance(user_root1.password, bytes) and isinstance(usr_root2.password, bytes)
        assert passwd_is_valid
        assert user_root1 == usr_root2

