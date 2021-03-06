"""

Revision ID: 9a0dd7bca5ef
Revises: bd398edb7d68
Create Date: 2020-06-19 22:21:19.814725

"""
import datetime

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '9a0dd7bca5ef'
down_revision = 'bd398edb7d68'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('program', sa.Column('created_at', sa.DateTime(), nullable=True))
    op.add_column('program', sa.Column('deleted_at', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('program', 'deleted_at')
    op.drop_column('program', 'created_at')
    # ### end Alembic commands ###
