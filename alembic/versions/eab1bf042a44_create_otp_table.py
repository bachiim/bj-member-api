"""create otp table

Revision ID: eab1bf042a44
Revises: 37dbde7b6a88
Create Date: 2025-07-07 13:40:35.294068

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'eab1bf042a44'
down_revision: Union[str, None] = '37dbde7b6a88'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table("otp",
        sa.Column("id", sa.INTEGER, primary_key=True),
        sa.Column("email", sa.VARCHAR(100), nullable=False, unique=True),
        sa.Column("kode_otp", sa.VARCHAR(6), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("expired_at", sa.DateTime(), nullable=False)
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("otp")
