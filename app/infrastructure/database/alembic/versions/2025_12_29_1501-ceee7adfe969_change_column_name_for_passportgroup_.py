"""change column name for PassportGroup table

Revision ID: ceee7adfe969
Revises: fc73b841fc9f
Create Date: 2025-12-29 15:01:04.746534

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "ceee7adfe969"
down_revision: Union[str, Sequence[str], None] = "fc73b841fc9f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "passport_groups", sa.Column("name", sa.String(length=32), nullable=True)
    )
    op.drop_constraint(
        op.f("uq_passport_groups_group_name"), "passport_groups", type_="unique"
    )
    op.create_unique_constraint(
        op.f("uq_passport_groups_name"), "passport_groups", ["name"]
    )
    op.drop_column("passport_groups", "group_name")


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column(
        "passport_groups",
        sa.Column("group_name", sa.VARCHAR(), autoincrement=False, nullable=False),
    )
    op.drop_constraint(
        op.f("uq_passport_groups_name"), "passport_groups", type_="unique"
    )
    op.create_unique_constraint(
        op.f("uq_passport_groups_group_name"),
        "passport_groups",
        ["group_name"],
        postgresql_nulls_not_distinct=False,
    )
    op.drop_column("passport_groups", "name")
