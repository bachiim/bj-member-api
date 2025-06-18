"""create jenis table

Revision ID: 85d28103aa80
Revises: cdb7f10ce425
Create Date: 2025-06-12 16:41:30.819262

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '85d28103aa80'
down_revision: Union[str, None] = 'cdb7f10ce425'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table("jenis",
        sa.Column("id", sa.SMALLINT(), primary_key=True),
        sa.Column("nama", sa.VARCHAR(50), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False)
    )

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("jenis")
