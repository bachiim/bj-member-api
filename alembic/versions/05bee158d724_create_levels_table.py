"""create levels table

Revision ID: 05bee158d724
Revises: 780f2dcdd2ca
Create Date: 2025-06-12 16:37:31.838433

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '05bee158d724'
down_revision: Union[str, None] = '780f2dcdd2ca'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table("levels",
        sa.Column("id", sa.SMALLINT(), primary_key=True),
        sa.Column("nama", sa.VARCHAR(50), nullable=False),
        sa.Column("potongan", sa.FLOAT(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False)
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("levels")
