"""create posts table

Revision ID: 046a91f3da1a
Revises: 
Create Date: 2023-03-12 21:20:36.687498

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '046a91f3da1a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.Integer(),
                    nullable=False, primary_key=True), sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
