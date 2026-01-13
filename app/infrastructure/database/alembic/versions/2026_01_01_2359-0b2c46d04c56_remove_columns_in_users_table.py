"""remove columns in Users table

Revision ID: 0b2c46d04c56
Revises: 4dccc0000006
Create Date: 2026-01-01 23:59:46.492314

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "0b2c46d04c56"
down_revision: Union[str, Sequence[str], None] = "4dccc0000006"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_column("users", "is_superuser")
    op.drop_column("users", "is_admin")


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column(
        "users",
        sa.Column(
            "is_admin",
            sa.BOOLEAN(),
            server_default=sa.text("false"),
            autoincrement=False,
            nullable=False,
        ),
    )
    op.add_column(
        "users",
        sa.Column(
            "is_superuser",
            sa.BOOLEAN(),
            server_default=sa.text("false"),
            autoincrement=False,
            nullable=False,
        ),
    )
