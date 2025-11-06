"""create TrafficLightObject table

Revision ID: 2fc0df5677a0
Revises: 02220211904e
Create Date: 2025-11-06 18:47:10.908854

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2fc0df5677a0'
down_revision: Union[str, Sequence[str], None] = '02220211904e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_table(
        'traffic_light_objects',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('region', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=32), nullable=False),
        sa.Column('district', sa.String(), server_default='', nullable=False),
        sa.Column('street', sa.String(), nullable=False),
        sa.Column('ovim_in_use', sa.Boolean(), server_default='false', nullable=False),
        sa.Column(
            'construction_in_use', sa.Boolean(), server_default='false', nullable=False
        ),
        sa.Column(
            'description', sa.String(length=255), server_default='false', nullable=False
        ),
        sa.Column(
            'created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False
        ),
        sa.Column(
            'updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False
        ),
        sa.PrimaryKeyConstraint('name', 'id', name=op.f('pk_traffic_light_objects')),
        sa.UniqueConstraint('name', name=op.f('uq_traffic_light_objects_name')),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_table('traffic_light_objects')
    # ### end Alembic commands ###
