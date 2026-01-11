import sqlalchemy as sa
from sqlalchemy import String, text
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.database.models import Base
from .mixins import CreatedAtMixin, UpdatedAtMixin, IntegerIdPkMixin


class User(
    IntegerIdPkMixin,
    CreatedAtMixin,
    UpdatedAtMixin,
    Base,
):
    first_name: Mapped[str | None] = mapped_column(
        String(32), server_default=text('NULL'), default=None, nullable=True
    )
    last_name: Mapped[str | None] = mapped_column(
        String(32), server_default=text('NULL'), default=None, nullable=True
    )
    organization: Mapped[str] = mapped_column(String(32), nullable=False)
    username: Mapped[str] = mapped_column(
        String(32),
        unique=True,
        nullable=False,
    )
    email: Mapped[str | None] = mapped_column(
        String(32), unique=True, default=None, nullable=True, server_default=None
    )
    password: Mapped[bytes]
    is_active: Mapped[bool] = mapped_column(
        nullable=False,
        default=True,
        server_default=sa.sql.expression.true(),
    )
    role: Mapped[str] = mapped_column(String(32), nullable=False)
    phone_number: Mapped[str | None] = mapped_column(
        String(32), unique=True, server_default=None, default=None, nullable=True
    )
    telegram: Mapped[str | None] = mapped_column(
        String(32),
        unique=True,
        nullable=True,
        default=None,
        server_default=None,
    )
    description: Mapped[str] = mapped_column(
        nullable=False,
        server_default='',
        default='',
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
            f'is_active={self.is_active}'
            f')'
        )

    def __repr__(self):
        return f'{self.__class__.__name__}(id={self.id} username={self.username})'
