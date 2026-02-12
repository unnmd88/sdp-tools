"""create regions table

Revision ID: 91e4830d88b1
Revises: 372a1039165d
Create Date: 2026-02-12 18:57:31.204004

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "91e4830d88b1"
down_revision: Union[str, Sequence[str], None] = "372a1039165d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "regions",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("code", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=32), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_regions")),
        sa.UniqueConstraint("code", name=op.f("uq_regions_code")),
        sa.UniqueConstraint("name", name=op.f("uq_regions_name")),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("regions")
