"""add alambic column in posts table

Revision ID: e707a328aeeb
Revises: 7e766452dd3f
Create Date: 2022-03-14 19:18:40.954109

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e707a328aeeb'
down_revision = '7e766452dd3f'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("posts", sa.Column("alembic", sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column("posts", "alembic")
    pass
