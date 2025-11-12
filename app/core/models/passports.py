from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.dialects.postgresql.json import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models import Base
from core.models.mixins.integer_pk_id import IntegerIdPkMixin
from core.models.mixins.timestamp import StartAtMixin, FinishedAtMixin

if TYPE_CHECKING:
    from . import User
    from . import TrafficLightObject


class Passport(
    IntegerIdPkMixin,
    StartAtMixin,
    FinishedAtMixin,
    Base,
):
    tlo_id: Mapped[int] = mapped_column(
        ForeignKey('traffic_light_objects.id'),
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id'),
    )
    owner_id: Mapped[int] = mapped_column(
        ForeignKey('passports_owners.id'),
    )
    data = mapped_column(
        JSONB,
        nullable=True,
    )
    commit_message: Mapped[str] = mapped_column(
        Text,
        nullable=True,
    )
    editing_now: Mapped[bool] = mapped_column(
        server_default='true',
    )

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
            f'owner_id={self.owner_id} '
            f'editing_now={self.editing_now} '
            f'data={"{...}" if self.data else self.data} '
            f'user_id={self.user_id} '
            f'commit_message={self.commit_message}'
            f')'
        )


# class OvimPassport(
#     IntegerIdPkMixin,
#     CreatedAtMixin,
#     Base,
# ):
#     tlo_id: Mapped[int] = mapped_column(
#         ForeignKey('traffic_light_objects.id'),
#     )
#     user_id: Mapped[int] = mapped_column(
#         ForeignKey('users.id'),
#     )
#     data = mapped_column(
#         JSONB,
#         nullable=False,
#     )
#     commit_message: Mapped[str] = mapped_column(Text)
#
#
#     # tlo: Mapped["TrafficLightObject"] = relationship(
#     #     lazy="joined",
#     # )
#     # user: Mapped["User"] = relationship(
#     #     lazy="joined",
#     # )
#
#     def __repr__(self):
#         return (
#             f'{self.__class__.__name__}('
#             f'id={self.id} '
#             f'tlo_id={self.tlo_id} '
#             f'user_id={self.user_id} '
#             f'commit_message={self.commit_message}'
#             f')'
#         )