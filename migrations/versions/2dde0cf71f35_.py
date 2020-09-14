"""empty message

Revision ID: 2dde0cf71f35
Revises: d0e59dfacf25
Create Date: 2020-09-02 16:44:14.177166

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '2dde0cf71f35'
down_revision = 'd0e59dfacf25'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('order',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('order_code', sa.String(length=20), nullable=False),
    sa.Column('status', sa.String(length=80), nullable=False),
    sa.Column('time', sa.Integer(), nullable=False),
    sa.Column('brand', sa.String(length=170), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('order_code')
    )
    op.drop_index('order_code', table_name='comanda')
    op.drop_table('comanda')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('comanda',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('order_code', mysql.VARCHAR(length=20), nullable=False),
    sa.Column('status', mysql.VARCHAR(length=80), nullable=False),
    sa.Column('time', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('brand', mysql.VARCHAR(length=170), nullable=False),
    sa.Column('is_active', mysql.TINYINT(display_width=1), autoincrement=False, nullable=False),
    sa.CheckConstraint('(`is_active` in (0,1))', name='comanda_chk_1'),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_index('order_code', 'comanda', ['order_code'], unique=True)
    op.drop_table('order')
    # ### end Alembic commands ###
