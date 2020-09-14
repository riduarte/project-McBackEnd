"""empty message

Revision ID: 5b871926e80b
Revises: 
Create Date: 2020-08-31 10:38:14.073656

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5b871926e80b'
down_revision = None
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
    sa.UniqueConstraint('email')
    )
    op.create_table('order',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('order_code', sa.String(length=20), nullable=False),
    sa.Column('status', sa.String(length=80), nullable=False),
    sa.Column('time', sa.Integer(), nullable=False),
    sa.Column('brand', sa.String(length=170), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('cooker_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['cooker_id'], ['cooker.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('brand'),
    sa.UniqueConstraint('order_code')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('order')
    op.drop_table('cooker')
    # ### end Alembic commands ###
