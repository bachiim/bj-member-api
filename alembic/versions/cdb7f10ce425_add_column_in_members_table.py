"""add column in members table

Revision ID: cdb7f10ce425
Revises: 05bee158d724
Create Date: 2025-06-12 16:39:32.067736

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cdb7f10ce425'
down_revision: Union[str, None] = '05bee158d724'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("members",
        sa.Column("id_level", sa.SMALLINT(), sa.ForeignKey("levels.id"), nullable=False)              
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("members", "id_level")
