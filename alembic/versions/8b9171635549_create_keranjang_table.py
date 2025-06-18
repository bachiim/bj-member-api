"""create keranjang table

Revision ID: 8b9171635549
Revises: a6eabcee3823
Create Date: 2025-06-12 16:45:15.524185

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8b9171635549'
down_revision: Union[str, None] = 'a6eabcee3823'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table("keranjang",
        sa.Column("id", sa.INTEGER(), primary_key=True),
        sa.Column("id_member", sa.INTEGER(), sa.ForeignKey("members.id"), nullable=False),
        sa.Column("id_item", sa.VARCHAR(100), sa.ForeignKey("items.id"), nullable=False),
        sa.Column("id_satuan", sa.SMALLINT(), sa.ForeignKey("satuan.id"), nullable=False),
        sa.Column("jumlah", sa.SMALLINT(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False)
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("keranjang")
