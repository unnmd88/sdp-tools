"""create Passport  table

Revision ID: 162ac5fc7b3b
Revises: 2b8baff9d9d4
Create Date: 2025-11-17 13:17:58.882997

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '162ac5fc7b3b'
down_revision: str | Sequence[str] | None = '2b8baff9d9d4'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'passports',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('tlo_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('group_id', sa.Integer(), nullable=False),
        sa.Column('data', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('commit_message', sa.Text(), nullable=True),
        sa.Column('editing_now', sa.Boolean(), server_default='true', nullable=False),
        sa.Column(
            'started_editing_at',
            sa.DateTime(),
            server_default=sa.text('now()'),
            nullable=False,
        ),
        sa.Column('finished_editing_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ['group_id'],
            ['passport_groups.id'],
            name=op.f('fk_passports_group_id_passport_groups'),
        ),
        sa.ForeignKeyConstraint(
            ['tlo_id'],
            ['traffic_light_objects.id'],
            name=op.f('fk_passports_tlo_id_traffic_light_objects'),
        ),
        sa.ForeignKeyConstraint(
            ['user_id'], ['users.id'], name=op.f('fk_passports_user_id_users')
        ),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_passports')),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('passports')
