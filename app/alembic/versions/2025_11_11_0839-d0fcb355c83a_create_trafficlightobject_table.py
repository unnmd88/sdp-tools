"""create TrafficLightObject table

Revision ID: d0fcb355c83a
Revises: edbaad25bbfe
Create Date: 2025-11-11 08:39:48.847490

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd0fcb355c83a'
down_revision: Union[str, Sequence[str], None] = 'edbaad25bbfe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_table(
        'traffic_light_objects',
        sa.Column(
            'id',
            sa.Integer(),
            autoincrement=True,
            nullable=False,
        ),
        sa.Column(
            'region_id',
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            'name',
            sa.String(length=32),
            nullable=False,
        ),
        sa.Column(
            'district',
            sa.String(),
            server_default='',
            nullable=False,
        ),
        sa.Column(
            'street',
            sa.Text(),
            nullable=False,
        ),
        sa.Column(
            'service_organization',
            sa.String(length=32),
            server_default='',
            nullable=False,
        ),
        sa.Column(
            'description',
            sa.Text(),
            server_default='',
            nullable=False,
        ),
        sa.Column(
            'ovim_passport_editing',
            sa.Boolean(),
            server_default='false',
            nullable=False,
        ),
        sa.Column(
            'stroykontrol_passport_editing',
            sa.Boolean(),
            server_default='false',
            nullable=False,
        ),
        sa.Column(
            'created_at',
            sa.DateTime(),
            server_default=sa.text('now()'),
            nullable=False,
        ),
        sa.Column(
            'updated_at',
            sa.DateTime(),
            server_default=sa.text('now()'),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ['region_id'],
            ['regions.id'],
            name=op.f('fk_traffic_light_objects_region_id_regions'),
        ),
        sa.PrimaryKeyConstraint(
            'id',
            name=op.f('pk_traffic_light_objects'),
        ),
        sa.UniqueConstraint(
            'name',
            name=op.f('uq_traffic_light_objects_name'),
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_table('traffic_light_objects')

