"""create PassportGroups table

Revision ID: aef9ff824d74
Revises: d0fcb355c83a
Create Date: 2025-11-16 13:38:34.769348

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'aef9ff824d74'
down_revision: Union[str, Sequence[str], None] = 'd0fcb355c83a'
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
