"""

Revision ID: abb9ddccf3d3
Revises: 
Create Date: 2020-06-19 19:36:45.775288

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'abb9ddccf3d3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'config',
        sa.Column('key', sa.String(length=25), nullable=False),
        sa.Column('type', sa.String(length=25), nullable=False),
        sa.Column('value', sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint('key'),
    )
    op.create_index(op.f('ix_config_key'), 'config', ['key'], unique=False)
    op.create_table(
        'parameter',
        sa.Column('parameter_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=25), nullable=False),
        sa.Column('type', sa.String(length=25), nullable=False),
        sa.Column('value', sa.String(length=100), nullable=False),
        sa.Column('weight', sa.Float(), nullable=False),
        sa.PrimaryKeyConstraint('parameter_id'),
    )
    op.create_index(op.f('ix_parameter_parameter_id'), 'parameter', ['parameter_id'], unique=False)
    op.create_table(
        'program',
        sa.Column('program_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=25), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('hours', sa.Integer(), nullable=True),
        sa.Column('is_minor', sa.Boolean(), nullable=False),
        sa.Column('category', sa.String(length=25), nullable=True),
        sa.PrimaryKeyConstraint('program_id'),
    )
    op.create_index(op.f('ix_program_category'), 'program', ['category'], unique=False)
    op.create_index(op.f('ix_program_name'), 'program', ['name'], unique=False)
    op.create_index(op.f('ix_program_program_id'), 'program', ['program_id'], unique=False)
    op.create_table(
        'program_to_parameter',
        sa.Column('left_id', sa.Integer(), nullable=False),
        sa.Column('right_id', sa.Integer(), nullable=False),
        sa.Column('weight', sa.Float(), nullable=True),
        sa.Column('value', sa.String(length=25), nullable=True),
        sa.ForeignKeyConstraint(['left_id'], ['parameter.parameter_id'],),
        sa.ForeignKeyConstraint(['right_id'], ['program.program_id'],),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('program_to_parameter')
    op.drop_index(op.f('ix_program_program_id'), table_name='program')
    op.drop_index(op.f('ix_program_name'), table_name='program')
    op.drop_index(op.f('ix_program_category'), table_name='program')
    op.drop_table('program')
    op.drop_index(op.f('ix_parameter_parameter_id'), table_name='parameter')
    op.drop_table('parameter')
    op.drop_index(op.f('ix_config_key'), table_name='config')
    op.drop_table('config')
    # ### end Alembic commands ###
