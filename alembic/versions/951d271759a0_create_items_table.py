"""create items table

Revision ID: 951d271759a0
Revises: 8b6784ca4614
Create Date: 2025-06-12 16:43:30.905095

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '951d271759a0'
down_revision: Union[str, None] = '8b6784ca4614'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table("items",
        sa.Column("id", sa.VARCHAR(100), primary_key=True),
        sa.Column("nama", sa.VARCHAR(100), nullable=False),
        sa.Column("url_gambar", sa.VARCHAR(), nullable=True),
        sa.Column("deskripsi", sa.TEXT(), nullable=True),
        sa.Column("id_jenis", sa.SMALLINT(), sa.ForeignKey("jenis.id"), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False)
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("items")
