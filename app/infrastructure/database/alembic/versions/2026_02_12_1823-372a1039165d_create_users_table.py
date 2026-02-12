"""create users table

Revision ID: 372a1039165d
Revises:
Create Date: 2026-02-12 18:23:47.676277

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "372a1039165d"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column(
            "first_name",
            sa.String(length=32),
            server_default=sa.text("NULL"),
            nullable=True,
        ),
        sa.Column(
            "last_name",
            sa.String(length=32),
            server_default=sa.text("NULL"),
            nullable=True,
        ),
        sa.Column("organization", sa.String(length=32), nullable=False),
        sa.Column("username", sa.String(length=32), nullable=False),
        sa.Column("email", sa.String(length=32), nullable=True),
        sa.Column("password", sa.LargeBinary(), nullable=False),
        sa.Column(
            "is_active", sa.Boolean(), server_default=sa.text("true"), nullable=False
        ),
        sa.Column("role", sa.String(length=32), nullable=False),
        sa.Column("phone_number", sa.String(length=32), nullable=True),
        sa.Column("telegram", sa.String(length=32), nullable=True),
        sa.Column("description", sa.String(), server_default="", nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_users")),
        sa.UniqueConstraint("email", name=op.f("uq_users_email")),
        sa.UniqueConstraint("phone_number", name=op.f("uq_users_phone_number")),
        sa.UniqueConstraint("telegram", name=op.f("uq_users_telegram")),
        sa.UniqueConstraint("username", name=op.f("uq_users_username")),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("users")
