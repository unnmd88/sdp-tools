from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models import Base
from core.models.mixins.integer_pk_id import IntegerIdPkMixin
from core.models.mixins.timestamp import CreatedAtMixin, UpdatedAtMixin


if TYPE_CHECKING:
    from . import TrafficLightObject


class Region(
    IntegerIdPkMixin,
    CreatedAtMixin,
    UpdatedAtMixin,
    Base,
):
    code: Mapped[int] = mapped_column(
        unique=True,
    )
    name: Mapped[str] = mapped_column(
        String(32),
        unique=True,
    )

    # user: Mapped["TrafficLightObject"] = relationship(
    #     back_populates="region",
    # )
