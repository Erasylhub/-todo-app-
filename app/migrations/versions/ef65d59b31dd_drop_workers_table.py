"""drop workers table

Revision ID: ef65d59b31dd
Revises: 9502c94199e8
Create Date: 2026-01-06 19:24:06.257906

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ef65d59b31dd'
down_revision: Union[str, Sequence[str], None] = '9502c94199e8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Удаляем таблицу workers."""
    op.drop_table('workers')


def downgrade() -> None:
    """Восстанавливаем таблицу workers при откате."""
    op.create_table(
        'workers',
        sa.Column('id', sa.INTEGER(), primary_key=True, autoincrement=True, nullable=False),
        sa.Column('username', sa.VARCHAR(), nullable=False)
    )
