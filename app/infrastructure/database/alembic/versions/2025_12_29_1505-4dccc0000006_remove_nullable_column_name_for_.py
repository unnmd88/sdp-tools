"""remove nullable column 'name' for PassportGroup table

Revision ID: 4dccc0000006
Revises: ceee7adfe969
Create Date: 2025-12-29 15:05:35.230653

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4dccc0000006'
down_revision: Union[str, Sequence[str], None] = 'ceee7adfe969'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        'passport_groups', 'name', existing_type=sa.VARCHAR(length=32), nullable=False
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        'passport_groups', 'name', existing_type=sa.VARCHAR(length=32), nullable=True
    )
