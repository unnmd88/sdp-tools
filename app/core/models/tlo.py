from sqlalchemy import String
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
    region: Mapped[int]
    name: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        unique=True,
        primary_key=True,
    )
    district: Mapped[str] = mapped_column(
        default='',
        server_default='',
    )
    street: Mapped[str] = mapped_column(
        nullable=False,
    )
    ovim_in_use: Mapped[bool] = mapped_column(
        default=False,
        server_default='false',
    )
    construction_in_use: Mapped[bool] = mapped_column(
        default=False,
        server_default='false',
    )
    description: Mapped[str] = mapped_column(
        String(255),
        default=False,
        server_default='false',
    )
