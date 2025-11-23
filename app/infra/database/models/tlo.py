from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infra.database import Base

from infra.database.models.mixins.integer_pk_id import IntegerIdPkMixin
from infra.database.models.mixins.timestamp import CreatedAtMixin, UpdatedAtMixin

if TYPE_CHECKING:
    from core.models import Region


class TrafficLightObject(
    IntegerIdPkMixin,
    CreatedAtMixin,
    UpdatedAtMixin,
    Base,
):
    region_id: Mapped[int] = mapped_column(
        ForeignKey('regions.id'),
    )
    name: Mapped[str] = mapped_column(
        String(32),
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
    service_organization: Mapped[str] = mapped_column(
        String(32),
        default='',
        server_default='',
    )
    description: Mapped[str] = mapped_column(
        Text,
        default='',
        server_default='',
    )
    region: Mapped['Region'] = relationship()
