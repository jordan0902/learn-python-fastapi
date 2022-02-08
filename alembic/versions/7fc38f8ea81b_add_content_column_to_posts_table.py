"""add content column to posts table

Revision ID: 7fc38f8ea81b
Revises: 1a731578eb30
Create Date: 2022-02-07 13:42:33.983687

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7fc38f8ea81b'
down_revision = '1a731578eb30'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(),nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
