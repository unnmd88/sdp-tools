"""remove group_name_route column in PassportGroup table

Revision ID: e68ea444cf4e
Revises: 162ac5fc7b3b
Create Date: 2025-12-25 20:01:51.615285

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e68ea444cf4e'
down_revision: Union[str, Sequence[str], None] = '162ac5fc7b3b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_constraint(
        op.f('uq_passport_groups_group_name_route'), 'passport_groups', type_='unique'
    )
    op.drop_column('passport_groups', 'group_name_route')


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column(
        'passport_groups',
        sa.Column(
            'group_name_route',
            sa.VARCHAR(length=32),
            autoincrement=False,
            nullable=False,
        ),
    )
    op.create_unique_constraint(
        op.f('uq_passport_groups_group_name_route'),
        'passport_groups',
        ['group_name_route'],
        postgresql_nulls_not_distinct=False,
    )
