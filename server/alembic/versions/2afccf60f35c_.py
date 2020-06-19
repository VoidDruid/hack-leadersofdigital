"""

Revision ID: 2afccf60f35c
Revises: 32a80059fe98
Create Date: 2020-06-19 23:04:25.400952

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '2afccf60f35c'
down_revision = '32a80059fe98'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        'discipline',
        sa.Column('parameters', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    )
    op.drop_column('program_to_discipline', 'parameters')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        'program_to_discipline',
        sa.Column(
            'parameters',
            postgresql.JSONB(astext_type=sa.Text()),
            autoincrement=False,
            nullable=True,
        ),
    )
    op.drop_column('discipline', 'parameters')
    # ### end Alembic commands ###