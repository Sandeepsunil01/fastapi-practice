"""Create Post Table

Revision ID: 067959dc97dc
Revises: 
Create Date: 2023-08-12 12:30:18.823926

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# https://alembic.sqlalchemy.org/en/latest/api/ddl.html #to Get all database migration guide

# revision identifiers, used by Alembic.
revision: str = '067959dc97dc'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('post', sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('title', sa.String(), nullable=False),
                    sa.Column('content', sa.String(), nullable=False)
                )
    pass

def downgrade() -> None:
    op.drop_table("posts")
    pass
