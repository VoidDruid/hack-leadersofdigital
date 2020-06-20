"""

Revision ID: 53a43f563d08
Revises: 3b908553fed5
Create Date: 2020-06-20 09:35:14.272297

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import datetime
# revision identifiers, used by Alembic.
revision = '53a43f563d08'
down_revision = '3b908553fed5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("UPDATE program SET created_at = current_timestamp")
    op.alter_column('program', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('program', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    # ### end Alembic commands ###
