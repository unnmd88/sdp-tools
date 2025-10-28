from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class IntegerIdPkMixin:
    id: Mapped[int] = mapped_column(primary_key=True)
