"""create sales table

Revision ID: 2b507bf44be1
Revises: 
Create Date: 2025-06-04 12:36:34.968123

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2b507bf44be1'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table("sales",
        sa.Column("id", sa.INTEGER(), primary_key=True),
        sa.Column("nama", sa.VARCHAR(100), nullable=False),
        sa.Column("alamat", sa.TEXT(), nullable=False),
        sa.Column("telepon", sa.VARCHAR(12), nullable=False, unique=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False)
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("sales")
