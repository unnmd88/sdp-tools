from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from core.models import Base
import sqlalchemy as sa

from core.models.mixins.integer_pk_id import IntegerIdPkMixin
from core.models.mixins.timestamp import UpdatedAtMixin, CreatedAtMixin


class User(IntegerIdPkMixin,CreatedAtMixin, UpdatedAtMixin, Base,):

    first_name: Mapped[str] = mapped_column(String(32), nullable=False,)
    last_name: Mapped[str] = mapped_column(String(32), nullable=False,)
    organization: Mapped[str] = mapped_column(String(32), nullable=False)
    username: Mapped[str] = mapped_column(String(32), unique=True, nullable=False,)
    email: Mapped[str] = mapped_column(unique=True, nullable=False, default='', server_default='',)
    password: Mapped[bytes] = mapped_column(unique=True, nullable=False,)
    is_active: Mapped[bool] = mapped_column(nullable=False, default=True, server_default=sa.sql.expression.true(),)
    is_admin: Mapped[bool] = mapped_column(nullable=False, default=True, server_default=sa.sql.expression.false(),)
    is_superuser: Mapped[bool] = mapped_column(nullable=False, default=True, server_default=sa.sql.expression.false(),)
    role: Mapped[str] = mapped_column(String(32), nullable=False)
    phone_number: Mapped[str] = mapped_column(String(32), nullable=False, default='', server_default='')
    telegram: Mapped[str] = mapped_column(String(32), nullable=False, default='', server_default='')
    description: Mapped[str] = mapped_column(nullable=False, default='', server_default='',)

    # foo: Mapped[int]
    # bar: Mapped[int]
    #
    # __table_args__ = (
    #     UniqueConstraint('foo', 'bar'),
    # )

