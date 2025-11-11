from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.dialects.postgresql.json import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models import Base
from core.models.mixins.integer_pk_id import IntegerIdPkMixin
from core.models.mixins.timestamp import CreatedAtMixin

if TYPE_CHECKING:
    from . import User
    from . import TrafficLightObject


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


    # tlo: Mapped["TrafficLightObject"] = relationship(
    #     lazy="joined",
    # )
    # user: Mapped["User"] = relationship(
    #     lazy="joined",
    # )

    def __repr__(self):
        return (
            f'{self.__class__.__name__}('
            f'id={self.id} '
            f'tlo_id={self.tlo_id} '
            f'user_id={self.user_id} '
            f'commit_message={self.commit_message}'
            f')'
        )