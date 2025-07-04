"""create pembayaran table

Revision ID: 37dbde7b6a88
Revises: 52872ac06b5f
Create Date: 2025-06-27 08:17:29.736918

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '37dbde7b6a88'
down_revision: Union[str, None] = '52872ac06b5f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table("pembayaran",
        sa.Column("id", sa.INTEGER, primary_key=True),
        sa.Column("id_transaksi", sa.INTEGER, sa.ForeignKey("transaksi.id"), nullable=False),
        sa.Column("bukti_transfer", sa.VARCHAR, nullable=False),
        sa.Column("total", sa.INTEGER, nullable=False),
        sa.Column("status", sa.VARCHAR(30), nullable=False),
        sa.Column("keterangan", sa.TEXT, nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("pembayaran")
