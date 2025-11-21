from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from core.models import Base
from core.models.mixins.integer_pk_id import IntegerIdPkMixin
from core.models.mixins.timestamp import CreatedAtMixin, UpdatedAtMixin


class PassportGroup(
    IntegerIdPkMixin,
    CreatedAtMixin,
    UpdatedAtMixin,
    Base,
):
    group_name: Mapped[str] = mapped_column(
        unique=True,
    )
    group_name_route: Mapped[str] = mapped_column(
        String(length=32),
        unique=True,
    )
    description: Mapped[str] = mapped_column(
        Text,
        default='',
        server_default='',
    )
