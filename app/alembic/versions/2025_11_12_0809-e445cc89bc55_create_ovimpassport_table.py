"""create OvimPassport table

Revision ID: e445cc89bc55
Revises: d0fcb355c83a
Create Date: 2025-11-12 08:09:00.293299

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'e445cc89bc55'
down_revision: Union[str, Sequence[str], None] = 'd0fcb355c83a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'ovim_passports',
        sa.Column(
            'id',
            sa.Integer(),
            autoincrement=True,
            nullable=False,
        ),
        sa.Column(
            'tlo_id',
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            'user_id',
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            'data',
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=True,
        ),
        sa.Column(
            'commit_message',
            sa.Text(),
            nullable=True,
        ),
        sa.Column(
            'editing_now',
            sa.Boolean(),
            server_default='true',
            nullable=False,
        ),
        sa.Column(
            'started_editing_at',
            sa.DateTime(),
            server_default=sa.text('now()'),
            nullable=False,
        ),
        sa.Column(
            'finished_editing_at',
            sa.DateTime(),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ['tlo_id'],
            ['traffic_light_objects.id'],
            name=op.f('fk_ovim_passports_tlo_id_traffic_light_objects'),
        ),
        sa.ForeignKeyConstraint(
            ['user_id'],
            ['users.id'],
            name=op.f('fk_ovim_passports_user_id_users'),
        ),
        sa.PrimaryKeyConstraint(
            'id',
            name=op.f('pk_ovim_passports'),
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('ovim_passports')
