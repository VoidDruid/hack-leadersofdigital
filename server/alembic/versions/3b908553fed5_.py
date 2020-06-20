"""

Revision ID: 3b908553fed5
Revises: 3297ec96b5c6
Create Date: 2020-06-20 08:22:21.852942

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '3b908553fed5'
down_revision = '3297ec96b5c6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'program_template_to_discipline',
        sa.Column('discipline_id', sa.Integer(), nullable=False),
        sa.Column('program_template_id', sa.Integer(), nullable=False),
        sa.Column('hours', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['discipline_id'], ['discipline.discipline_id'],),
        sa.ForeignKeyConstraint(['program_template_id'], ['program_template.program_template_id'],),
        sa.PrimaryKeyConstraint('discipline_id', 'program_template_id'),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('program_template_to_discipline')
    # ### end Alembic commands ###
