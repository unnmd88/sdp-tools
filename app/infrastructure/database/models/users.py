import sqlalchemy as sa
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.database.models import Base
from .mixins import CreatedAtMixin, UpdatedAtMixin, IntegerIdPkMixin


class User(
    IntegerIdPkMixin,
    CreatedAtMixin,
    UpdatedAtMixin,
    Base,
):
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

    def __str__(self):
        return (
            f'{self.__class__.__name__}('
            f'id={self.id} '
            f'first_name={self.first_name} '
            f'last_name={self.last_name} '
            f'username={self.username} '
            f'role={self.role} '
            f'organization={self.organization} '
            f'email={self.email} '
            f'is_active={self.is_active} '
            f'is_admin={self.is_admin} '
            f'is_superuser={self.is_superuser} '
            f')'
        )

    def __repr__(self):
        return f'{self.__class__.__name__}(id={self.id} username={self.username})'
