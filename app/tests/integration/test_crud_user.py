import pytest
from sqlalchemy.ext.asyncio.session import AsyncSession

from core.models import User
"""
    first_name: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
    )
    last_name: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
    )
    organization: Mapped[str] = mapped_column(String(32), nullable=False)
    username: Mapped[str] = mapped_column(
        String(32),
        unique=True,
        nullable=False,
    )
    email: Mapped[str] = mapped_column(
        # unique=True,
        nullable=False,
        default='',
        server_default='',
    )
    password: Mapped[bytes] = mapped_column(
        # unique=True,
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(
        nullable=False,
        default=True,
        server_default=sa.sql.expression.true(),
    )
    is_admin: Mapped[bool] = mapped_column(
        nullable=False,
        default=True,
        server_default=sa.sql.expression.false(),
    )
    is_superuser: Mapped[bool] = mapped_column(
        nullable=False,
        default=True,
        server_default=sa.sql.expression.false(),
    )
    role: Mapped[str] = mapped_column(String(32), nullable=False)
    phone_number: Mapped[str] = mapped_column(
        String(32), nullable=False, default='', server_default=''
    )
    telegram: Mapped[str] = mapped_column(
        String(32), nullable=False, default='', server_default=''
    )
    description: Mapped[str] = mapped_column(
        nullable=False,
        default='',
        server_default='',
    )

"""

@pytest.mark.asyncio(loop_scope="session")
async def test_create_user(t_session: AsyncSession):
    print(f'{type(t_session)=}')
    new_user = User(
        first_name='chook',
        last_name='gekk',
        organization='SDP',
        username='chook@gekk',
        password=b'password1',
        is_active=True,
        is_admin=True,
        is_superuser=True,
        role='superman',
    )

    t_session.add(new_user)
    await t_session.commit()
    # await t_session.refresh(new_user)



    print(new_user)