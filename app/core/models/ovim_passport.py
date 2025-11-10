from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.dialects.postgresql.json import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from core.models import Base
from core.models.mixins.integer_pk_id import IntegerIdPkMixin
from core.models.mixins.timestamp import CreatedAtMixin


class OvimPassport(
    IntegerIdPkMixin,
    CreatedAtMixin,
    Base,
):
    tlo_id: Mapped[int] = mapped_column(
        ForeignKey('traffic_light_objects.id'),
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id'),
    )
    data = mapped_column(
        JSONB,
        nullable=False,
    )
    commit_message: Mapped[str] = mapped_column(Text)
