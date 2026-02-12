"""create trafficlight objects table

Revision ID: cf8b8e2c3827
Revises: 34ba5aec79cf
Create Date: 2026-02-13 00:20:57.249321

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "cf8b8e2c3827"
down_revision: Union[str, Sequence[str], None] = "34ba5aec79cf"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "traffic_light_objects",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("region_id", sa.Integer(), nullable=False),
        sa.Column("created_by_user_id", sa.Integer(), nullable=False),
        sa.Column("updated_by_user_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=32), nullable=False),
        sa.Column("traffic_controller_type", sa.String(length=32), nullable=True),
        sa.Column("latitude", sa.Float(), server_default=sa.text("0"), nullable=False),
        sa.Column("longitude", sa.Float(), server_default=sa.text("0"), nullable=False),
        sa.Column("district", sa.String(), server_default="", nullable=False),
        sa.Column("address", sa.String(), server_default="", nullable=False),
        sa.Column("note", sa.String(), server_default="", nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["created_by_user_id"],
            ["users.id"],
            name=op.f("fk_traffic_light_objects_created_by_user_id_users"),
        ),
        sa.ForeignKeyConstraint(
            ["region_id"],
            ["regions.id"],
            name=op.f("fk_traffic_light_objects_region_id_regions"),
        ),
        sa.ForeignKeyConstraint(
            ["updated_by_user_id"],
            ["users.id"],
            name=op.f("fk_traffic_light_objects_updated_by_user_id_users"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_traffic_light_objects")),
        sa.UniqueConstraint("name", name=op.f("uq_traffic_light_objects_name")),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("traffic_light_objects")
