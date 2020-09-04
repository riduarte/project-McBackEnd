"""empty message

Revision ID: bc21c75a4937
Revises: c6e512ac0008
Create Date: 2020-09-03 09:33:13.055309

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'bc21c75a4937'
down_revision = 'c6e512ac0008'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cooker',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nickname', sa.String(length=80), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password', sa.String(length=80), nullable=False),
    sa.Column('enterprise', sa.String(length=100), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=False),
    sa.Column('last_name', sa.String(length=80), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('nickname')
    )
    op.create_table('called',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('called_code', sa.String(length=20), nullable=False),
    sa.Column('status', sa.String(length=80), nullable=False),
    sa.Column('time', sa.Integer(), nullable=False),
    sa.Column('brand', sa.String(length=170), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('parent_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['parent_id'], ['cooker.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('called_code')
    )
    op.drop_index('email', table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('email', mysql.VARCHAR(length=120), nullable=False),
    sa.Column('password', mysql.VARCHAR(length=80), nullable=False),
    sa.Column('is_active', mysql.TINYINT(display_width=1), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='latin1',
    mysql_engine='InnoDB'
    )
    op.create_index('email', 'user', ['email'], unique=True)
    op.drop_table('called')
    op.drop_table('cooker')
    # ### end Alembic commands ###
