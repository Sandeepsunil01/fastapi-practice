"""Add all remaining columns

Revision ID: 21b70c041af2
Revises: 215797799dff
Create Date: 2023-08-12 13:16:55.733856

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '21b70c041af2'
down_revision: Union[str, None] = '215797799dff'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('post', sa.Column(
        'published', sa.Boolean(), nullable=False, server_default='FALSE'))
    pass


def downgrade() -> None:
    op.drop_column('post', 'published')
    pass
