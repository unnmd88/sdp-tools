from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column

from core.models import Base
from core.models.mixins.integer_pk_id import IntegerIdPkMixin
from core.models.mixins.timestamp import CreatedAtMixin, UpdatedAtMixin


class PassportsOwner(
    IntegerIdPkMixin,
    CreatedAtMixin,
    UpdatedAtMixin,
    Base,
):
    owner: Mapped[str] = mapped_column(
        unique=True,
    )
    description: Mapped[str] = mapped_column(
        Text,
        default='',
        server_default='',
    )

