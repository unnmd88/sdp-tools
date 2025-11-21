from datetime import UTC, datetime

from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column


def get_current_dt() -> datetime:
    dt = datetime.now(tz=UTC)
    return dt.replace(microsecond=0, tzinfo=None)


class CreatedAtMixin:
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(),
        server_default=func.now(),
        default=get_current_dt,
    )


class UpdatedAtMixin:
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(),
        server_default=func.now(),
        onupdate=func.now(),
        server_onupdate=func.now(),
    )


class StartAtMixin:
    started_editing_at: Mapped[datetime] = mapped_column(
        default=datetime.now,
        server_default=func.now(),
    )


class FinishedAtMixin:
    finished_editing_at: Mapped[datetime | None]
