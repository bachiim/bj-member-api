"""create members table

Revision ID: 780f2dcdd2ca
Revises: 2b507bf44be1
Create Date: 2025-06-04 12:40:11.014181

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '780f2dcdd2ca'
down_revision: Union[str, None] = '2b507bf44be1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table("members",
        sa.Column("id", sa.INTEGER(), primary_key=True),
        sa.Column("nama", sa.VARCHAR(100), nullable=False),
        sa.Column("alamat", sa.TEXT(), nullable=False),
        sa.Column("telepon", sa.VARCHAR(12), nullable=False, unique=False),
        sa.Column("kota", sa.VARCHAR(50), nullable=False),
        sa.Column("email", sa.VARCHAR(100), nullable=False, unique=True),
        sa.Column("password", sa.VARCHAR(), nullable=False),
        sa.Column("ref_member", sa.INTEGER(), sa.ForeignKey("members.id"), nullable=True),
        sa.Column("ref_sales", sa.INTEGER(), sa.ForeignKey("sales.id"), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False)
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("members")
