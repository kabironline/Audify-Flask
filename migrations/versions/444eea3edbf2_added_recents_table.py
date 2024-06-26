"""Added Recents Table

Revision ID: 444eea3edbf2
Revises: 652af2a5d923
Create Date: 2023-11-18 16:16:46.502867

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '444eea3edbf2'
down_revision = '652af2a5d923'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Recent',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
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
    op.drop_table('Recent')
    # ### end Alembic commands ###
