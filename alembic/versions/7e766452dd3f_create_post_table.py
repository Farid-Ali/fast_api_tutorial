"""create post table

Revision ID: 7e766452dd3f
Revises: 
Create Date: 2022-03-14 00:04:43.730560

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7e766452dd3f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("posts", sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
                    sa.Column("title", sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_table("posts")
    pass
