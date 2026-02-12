"""create passport groups table

Revision ID: 34ba5aec79cf
Revises: 91e4830d88b1
Create Date: 2026-02-12 19:01:58.117281

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "34ba5aec79cf"
down_revision: Union[str, Sequence[str], None] = "91e4830d88b1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "passport_groups",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=32), nullable=False),
        sa.Column("description", sa.Text(), server_default="", nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_passport_groups")),
        sa.UniqueConstraint("name", name=op.f("uq_passport_groups_name")),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("passport_groups")
