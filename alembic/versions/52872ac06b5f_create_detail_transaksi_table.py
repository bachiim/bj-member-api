"""create detail transaksi table

Revision ID: 52872ac06b5f
Revises: da25c46e292c
Create Date: 2025-06-12 16:46:41.055565

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '52872ac06b5f'
down_revision: Union[str, None] = 'da25c46e292c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table("detail_transaksi",
        sa.Column("id", sa.INTEGER(), primary_key=True),
        sa.Column("id_transaksi", sa.INTEGER(), sa.ForeignKey("transaksi.id"), nullable=False),
        sa.Column("id_item", sa.VARCHAR(100), sa.ForeignKey("items.id"), nullable=False),
        sa.Column("id_satuan", sa.SMALLINT(), sa.ForeignKey("satuan.id"), nullable=False),
        sa.Column("jumlah", sa.SMALLINT(), nullable=False),
        sa.Column("harga", sa.INTEGER(), nullable=False),
        sa.Column("subtotal", sa.INTEGER(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False)
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("detail_transaksi")
