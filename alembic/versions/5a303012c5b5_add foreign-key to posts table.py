"""add foreign-key to posts table

Revision ID: 5a303012c5b5
Revises: 1995953f0ad3
Create Date: 2022-02-07 14:24:28.159897

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '5a303012c5b5'
down_revision = '1995953f0ad3'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(),nullable=False))
    op.create_foreign_key('post_users_fk',source_table="posts",referent_table="users",
        local_cols=['owner_id'],remote_cols=['id'],ondelete="CASCADE")
    pass

def downgrade():
    op.drop_constraint('post_users_fk',table_name="posts")
    op.drop_column('posts','owner_id')
    pass
