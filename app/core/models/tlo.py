from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from core.models import Base

from .mixins.integer_pk_id import IntegerIdPkMixin
from .mixins.timestamp import CreatedAtMixin, UpdatedAtMixin


class TrafficLightObject(
    IntegerIdPkMixin,
    CreatedAtMixin,
    UpdatedAtMixin,
    Base,
):
    region: Mapped[int] = mapped_column(unique=True, nullable=False,)
    name: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        unique=True,
    )
    district: Mapped[str] = mapped_column(
        default='',
        server_default='',
    )
    street: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    description: Mapped[str] = mapped_column(
        Text,
        default='',
        server_default='',
    )
    ovim_in_use: Mapped[bool] = mapped_column(
        default=False,
        server_default='false',
    )
    construction_in_use: Mapped[bool] = mapped_column(
        default=False,
        server_default='false',
    )

