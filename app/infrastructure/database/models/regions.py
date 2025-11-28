from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.database.models import Base

from infrastructure.database.models.mixins.integer_pk_id import IntegerIdPkMixin
from .mixins import CreatedAtMixin, UpdatedAtMixin

if TYPE_CHECKING:
    pass


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
