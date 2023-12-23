"""Add Foreign to post table

Revision ID: 215797799dff
Revises: 6e703668fff9
Create Date: 2023-08-12 13:09:39.669379

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '215797799dff'
down_revision: Union[str, None] = '6e703668fff9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('post', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table="post", referent_table="users", local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fk', 'post')
    op.drop_column('post', "owner_id")
    pass
