from datetime import UTC
from datetime import datetime as dt_datetime

from sqlalchemy import func, Column, DateTime
from sqlalchemy.orm import Mapped, mapped_column


def get_current_dt() -> dt_datetime:
    dt = dt_datetime.now(tz=UTC)
    return dt.replace(microsecond=0, tzinfo=None)


class CreatedAtMixin:

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(), server_default=func.now(), default=get_current_dt,
    )


class UpdatedAtMixin:

    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(), server_default=func.now(), onupdate=func.now(), server_onupdate=func.now(),
    )
