"""Added Created at column in post table

Revision ID: 89209af3d17b
Revises: 067959dc97dc
Create Date: 2023-08-12 12:55:24.086443

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '89209af3d17b'
down_revision: Union[str, None] = '067959dc97dc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('post', sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('post', 'created_at')
    pass
