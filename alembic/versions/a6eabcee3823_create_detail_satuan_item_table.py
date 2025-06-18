"""create detail satuan item table

Revision ID: a6eabcee3823
Revises: 951d271759a0
Create Date: 2025-06-12 16:44:17.447940

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a6eabcee3823'
down_revision: Union[str, None] = '951d271759a0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table("detail_satuan_item",
        sa.Column("id", sa.INTEGER(), primary_key=True),
        sa.Column("id_item", sa.VARCHAR(100), sa.ForeignKey("items.id"), nullable=False),
        sa.Column("id_satuan", sa.SMALLINT(), sa.ForeignKey("satuan.id"), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False)
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("detail_satuan_item")
