"""Added rating table

Revision ID: f51df18193ce
Revises: 90150e31c525
Create Date: 2023-11-14 00:51:52.302888

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f51df18193ce'
down_revision = '90150e31c525'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Rating',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('rating', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('track_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('last_modified_at', sa.DateTime(), nullable=False),
    sa.Column('created_by', sa.Integer(), nullable=False),
    sa.Column('last_modified_by', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['created_by'], ['User.id'], ),
    sa.ForeignKeyConstraint(['last_modified_by'], ['User.id'], ),
    sa.ForeignKeyConstraint(['track_id'], ['Track.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['User.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Rating')
    # ### end Alembic commands ###
