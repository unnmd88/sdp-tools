from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import UniqueConstraint

from core.models import Base


# class User(Base):
#     username: Mapped[str] = mapped_column(unique=True)
#     # foo: Mapped[int]
#     # bar: Mapped[int]
#     #
#     # __table_args__ = (
#     #     UniqueConstraint('foo', 'bar'),
#     # )

class User(Base):

    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column(unique=True)
    is_active: Mapped[bool]
    is_admin: Mapped[bool]

    # foo: Mapped[int]
    # bar: Mapped[int]
    #
    # __table_args__ = (
    #     UniqueConstraint('foo', 'bar'),
    # )