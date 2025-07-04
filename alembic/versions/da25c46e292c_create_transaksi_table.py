"""create transaksi table

Revision ID: da25c46e292c
Revises: 8b9171635549
Create Date: 2025-06-12 16:45:58.949183

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'da25c46e292c'
down_revision: Union[str, None] = '8b9171635549'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table("transaksi",
        sa.Column("id", sa.INTEGER(), primary_key=True),
        sa.Column("id_member", sa.INTEGER(), sa.ForeignKey("members.id"), nullable=False),
        sa.Column("id_pesanan", sa.VARCHAR(50), nullable=True, unique=True),
        sa.Column("tanggal", sa.DateTime(), nullable=False),
        sa.Column("potongan", sa.FLOAT(), nullable=False),
        sa.Column("subtotal", sa.INTEGER(), nullable=False),
        sa.Column("total", sa.INTEGER(), nullable=False),
        sa.Column("status", sa.VARCHAR(30), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("transaksi")
