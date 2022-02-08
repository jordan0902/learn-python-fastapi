"""add user table

Revision ID: 1995953f0ad3
Revises: 7fc38f8ea81b
Create Date: 2022-02-07 13:50:52.652701

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1995953f0ad3'
down_revision = '7fc38f8ea81b'
branch_labels = None
depends_on = None


def upgrade():  
    op.create_table('users',
        sa.Column('id',sa.Integer(),nullable=False),
        sa.Column('email',sa.String(),nullable=False),
        sa.Column('password',sa.String(),nullable=False),
        sa.Column('created_at',sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text('now()')),
        #set id as primaryKey
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
        )

    pass


def downgrade():
    op.drop_table('users')
    pass
