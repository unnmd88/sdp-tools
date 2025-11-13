"""create PassportsOwner table

Revision ID: 8bf2368dc83c
Revises: d0fcb355c83a
Create Date: 2025-11-12 18:05:08.102841

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8bf2368dc83c'
down_revision: Union[str, Sequence[str], None] = 'd0fcb355c83a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_table(
        'passports_owners',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('owner', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), server_default='', nullable=False),
        sa.Column(
            'created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False
        ),
        sa.Column(
            'updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False
        ),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_passports_owners')),
        sa.UniqueConstraint('owner', name=op.f('uq_passports_owners_owner')),
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_table('passports_owners')
