"""create PassportGroup table

Revision ID: 2b8baff9d9d4
Revises: 3ee3d6ea3f42
Create Date: 2025-11-17 12:57:01.414882

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2b8baff9d9d4'
down_revision: Union[str, Sequence[str], None] = '3ee3d6ea3f42'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'passport_groups',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('group_name', sa.String(), nullable=False),
        sa.Column('group_name_route', sa.String(length=32), nullable=False),
        sa.Column('description', sa.Text(), server_default='', nullable=False),
        sa.Column(
            'created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False
        ),
        sa.Column(
            'updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False
        ),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_passport_groups')),
        sa.UniqueConstraint('group_name', name=op.f('uq_passport_groups_group_name')),
        sa.UniqueConstraint(
            'group_name_route', name=op.f('uq_passport_groups_group_name_route')
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('passport_groups')
