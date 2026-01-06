from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '9502c94199e8'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # -----------------------------
    # Создание таблицы users
    # -----------------------------
    op.create_table(
        'users',
        sa.Column('id', sa.INTEGER(), primary_key=True, autoincrement=True, nullable=False),
        sa.Column('username', sa.VARCHAR(length=50), nullable=False, unique=True),
        sa.Column('email', sa.VARCHAR(length=100), nullable=False, unique=True),
        sa.Column('password', sa.VARCHAR(), nullable=False)
    )

    # -----------------------------
    # Создание таблицы todos
    # -----------------------------
    op.create_table(
        'todos',
        sa.Column('id', sa.INTEGER(), primary_key=True, autoincrement=True, nullable=False),
        sa.Column('title', sa.VARCHAR(), nullable=False),
        sa.Column('description', sa.VARCHAR(), nullable=True),
        sa.Column('completed', sa.BOOLEAN(), nullable=False, server_default=sa.text('false')),
        sa.Column('user_id', sa.INTEGER(), sa.ForeignKey('users.id'), nullable=False)
    )



def downgrade() -> None:
    # -----------------------------
    # Удаляем таблицы в обратном порядке
    # -----------------------------
    op.drop_table('todos')
    op.drop_table('workers')
    op.drop_table('users')