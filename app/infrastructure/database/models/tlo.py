from ipaddress import IPv4Address, IPv4Interface

from sqlalchemy import ForeignKey, String, Text, text
from sqlalchemy.dialects.postgresql import INET, CIDR
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.database.models import Base

from infrastructure.database.models.mixins.integer_pk_id import IntegerIdPkMixin
from infrastructure.database.models.mixins.timestamp import (
    CreatedAtMixin,
    UpdatedAtMixin,
)


class TrafficLightObject(
    IntegerIdPkMixin,
    CreatedAtMixin,
    UpdatedAtMixin,
    Base,
):
    region_id: Mapped[int] = mapped_column(
        ForeignKey("regions.id"),
    )
    created_by_user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
    )
    updated_by_user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
    )
    name: Mapped[str] = mapped_column(
        String(32),
        unique=True,
    )
    traffic_controller_type: Mapped[str] = mapped_column(
        String(32),
        nullable=True,
    )
    latitude: Mapped[float] = mapped_column(default=0, server_default=text("0"))
    longitude: Mapped[float] = mapped_column(default=0, server_default=text("0"))
    # ipv4: Mapped[IPv4Interface | None] = mapped_column(
    #     INET, server_default=text("Null"), default=None
    # )
    # gateway: Mapped[IPv4Interface | None] = mapped_column(
    #     INET, server_default=text("Null"), default=None
    # )
    # mac_address: Mapped[IPv4Address | None] = mapped_column(
    #     String(17), server_default=text("Null"), default=None
    # )
    district: Mapped[str] = mapped_column(
        default="",
        server_default="",
    )
    address: Mapped[str] = mapped_column(
        nullable=False,
        default="",
        server_default="",
    )
    note: Mapped[str] = mapped_column(
        default="",
        server_default="",
    )
