"""add last few columns to posts table

Revision ID: e815b2b002a9
Revises: 5a303012c5b5
Create Date: 2022-02-07 14:55:54.143258

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e815b2b002a9'
down_revision = '5a303012c5b5'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('published', sa.Boolean(),nullable=False,server_default='TRUE'))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True),
            nullable=False,server_default=sa.text('now()')))
    pass


def downgrade():
    op.drop_column('posts','published')
    op.drop_column('posts','created_at')
    pass
