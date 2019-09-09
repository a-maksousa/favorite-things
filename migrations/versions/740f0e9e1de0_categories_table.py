"""categories table

Revision ID: 740f0e9e1de0
Revises: 
Create Date: 2019-09-09 10:52:33.722205

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '740f0e9e1de0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('categories__lookup',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=30), nullable=False),
    sa.Column('cteated_date', sa.DateTime(), nullable=False),
    sa.Column('modified_date', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_categories__lookup_title'), 'categories__lookup', ['title'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_categories__lookup_title'), table_name='categories__lookup')
    op.drop_table('categories__lookup')
    # ### end Alembic commands ###