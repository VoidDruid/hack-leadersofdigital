"""

Revision ID: 2b7619c24cb4
Revises: 53a43f563d08
Create Date: 2020-06-20 19:19:52.480896

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '2b7619c24cb4'
down_revision = '53a43f563d08'
branch_labels = None
depends_on = None


def upgrade():
    ### commands manually generated by Vasiliy Kovalev - please adjust! ###
    op.alter_column(
        'parameter',
        'name',
        existing_type=sa.VARCHAR(length=25),
        type_=sa.String(length=100),
        existing_nullable=False,
    )
    ### end Alembic commands ###


def downgrade():
    ### commands manually generated by Vasiliy Kovalev - please adjust! ###
    op.alter_column(
        'parameter',
        'name',
        existing_type=sa.String(length=25),
        type_=sa.VARCHAR(length=100),
        existing_nullable=False,
    )
    ### end Alembic commands ###
