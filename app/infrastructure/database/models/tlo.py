from ipaddress import IPv4Address, IPv4Interface
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, Text, text
from sqlalchemy.dialects.postgresql import INET, CIDR
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.database.models import Base

from infrastructure.database.models.mixins.integer_pk_id import IntegerIdPkMixin
from infrastructure.database.models.mixins.timestamp import (
    CreatedAtMixin,
    UpdatedAtMixin,
)

if TYPE_CHECKING:
    from infrastructure.database.models import Region


class TrafficLightObject(
    IntegerIdPkMixin,
    CreatedAtMixin,
    UpdatedAtMixin,
    Base,
):
    name: Mapped[str] = mapped_column(
        String(32),
        unique=True,
    )
    region_id: Mapped[int] = mapped_column(
        ForeignKey("regions.id"),
    )
    latitude: Mapped[float] = mapped_column(default=0, server_default=text("0"))
    longitude: Mapped[float] = mapped_column(default=0, server_default=text("0"))
    ipv4: Mapped[IPv4Interface | None] = mapped_column(
        INET, server_default=text("Null"), default=None
    )
    gateway: Mapped[IPv4Interface | None] = mapped_column(
        INET, server_default=text("Null"), default=None
    )
    mac_address: Mapped[IPv4Address | None] = mapped_column(
        String(17), server_default=text("Null"), default=None
    )
    traffic_controller: Mapped[str | None]
    district: Mapped[str] = mapped_column(
        default="",
        server_default="",
    )
    street: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    service_organization: Mapped[str] = mapped_column(
        String(32),
        default="",
        server_default="",
    )
    description: Mapped[str] = mapped_column(
        Text,
        default="",
        server_default="",
    )
    # region: Mapped['Region'] = relationship()
