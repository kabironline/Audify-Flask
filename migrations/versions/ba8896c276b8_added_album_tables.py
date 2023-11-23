"""Added album tables

Revision ID: ba8896c276b8
Revises: f0587fa082ad
Create Date: 2023-11-22 13:34:55.596896

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ba8896c276b8'
down_revision = 'f0587fa082ad'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Album',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('release_date', sa.DateTime(), nullable=False),
    sa.Column('created_by', sa.Integer(), nullable=True),
    sa.Column('last_modified_by', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('last_modified_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['created_by'], ['User.id'], ),
    sa.ForeignKeyConstraint(['last_modified_by'], ['User.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('AlbumItem',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('album_id', sa.Integer(), nullable=False),
    sa.Column('track_id', sa.Integer(), nullable=False),
    sa.Column('created_by', sa.Integer(), nullable=True),
    sa.Column('last_modified_by', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('last_modified_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['album_id'], ['Album.id'], ),
    sa.ForeignKeyConstraint(['created_by'], ['User.id'], ),
    sa.ForeignKeyConstraint(['last_modified_by'], ['User.id'], ),
    sa.ForeignKeyConstraint(['track_id'], ['Track.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('AlbumItem')
    op.drop_table('Album')
    # ### end Alembic commands ###