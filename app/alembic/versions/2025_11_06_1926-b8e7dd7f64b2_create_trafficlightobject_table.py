"""create TrafficLightObject table

Revision ID: b8e7dd7f64b2
Revises: 02220211904e
Create Date: 2025-11-06 19:26:45.810685

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b8e7dd7f64b2'
down_revision: Union[str, Sequence[str], None] = '02220211904e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_table(
        'traffic_light_objects',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('region', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=32), nullable=False),
        sa.Column('district', sa.String(), server_default='', nullable=False),
        sa.Column('street', sa.String(), nullable=False),
        sa.Column('ovim_in_use', sa.Boolean(), server_default='false', nullable=False),
        sa.Column(
            'construction_in_use', sa.Boolean(), server_default='false', nullable=False
        ),
        sa.Column(
            'description', sa.String(length=255), server_default='', nullable=False
        ),
        sa.Column(
            'created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False
        ),
        sa.Column(
            'updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False
        ),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_traffic_light_objects')),
        sa.UniqueConstraint('name', name=op.f('uq_traffic_light_objects_name')),
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_table('traffic_light_objects')
