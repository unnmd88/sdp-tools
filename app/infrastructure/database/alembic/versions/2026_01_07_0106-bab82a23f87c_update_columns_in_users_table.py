"""update columns in Users table

Revision ID: bab82a23f87c
Revises: 0b2c46d04c56
Create Date: 2026-01-07 01:06:51.674316

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bab82a23f87c'
down_revision: Union[str, Sequence[str], None] = '0b2c46d04c56'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Alembic упорно генерировал миграцию с existing_server_default=sa.text("''::character varying")
# для колонок email, phone_number, telegram. Хотя ожидалось None(NULL).
# Руками установил значение None для existing_server_default вышеперечисленных полей.
# Также руками добавил length=32 в existing_type=sa.VARCHAR() для поля email.

def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        'users', 'first_name', existing_type=sa.VARCHAR(length=32), nullable=True
    )
    op.alter_column(
        'users', 'last_name', existing_type=sa.VARCHAR(length=32), nullable=True
    )
    op.alter_column(
        'users',
        'email',
        existing_type=sa.VARCHAR(length=32),
        nullable=True,
        existing_server_default=None,
    )
    op.alter_column(
        'users',
        'phone_number',
        existing_type=sa.VARCHAR(length=32),
        nullable=True,
        existing_server_default=None,
    )
    op.alter_column(
        'users',
        'telegram',
        existing_type=sa.VARCHAR(length=32),
        nullable=True,
        existing_server_default=None,
    )
    op.create_unique_constraint(op.f('uq_users_email'), 'users', ['email'])
    op.create_unique_constraint(
        op.f('uq_users_phone_number'), 'users', ['phone_number']
    )
    op.create_unique_constraint(op.f('uq_users_telegram'), 'users', ['telegram'])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(op.f('uq_users_telegram'), 'users', type_='unique')
    op.drop_constraint(op.f('uq_users_phone_number'), 'users', type_='unique')
    op.drop_constraint(op.f('uq_users_email'), 'users', type_='unique')
    op.alter_column(
        'users',
        'telegram',
        existing_type=sa.VARCHAR(length=32),
        nullable=False,
        existing_server_default=sa.text("''::character varying"),
    )
    op.alter_column(
        'users',
        'phone_number',
        existing_type=sa.VARCHAR(length=32),
        nullable=False,
        existing_server_default=sa.text("''::character varying"),
    )
    op.alter_column(
        'users',
        'email',
        existing_type=sa.VARCHAR(),
        nullable=False,
        existing_server_default=sa.text("''::character varying"),
    )
    op.alter_column(
        'users', 'last_name', existing_type=sa.VARCHAR(length=32), nullable=False
    )
    op.alter_column(
        'users', 'first_name', existing_type=sa.VARCHAR(length=32), nullable=False
    )
