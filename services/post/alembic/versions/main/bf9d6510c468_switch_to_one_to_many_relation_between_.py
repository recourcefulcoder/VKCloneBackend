"""switch to One-To-Many relation between posts and files

Revision ID: bf9d6510c468
Revises: 6b9c64dbf3cc
Create Date: 2025-03-27 14:01:35.975596

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bf9d6510c468'
down_revision: Union[str, None] = '6b9c64dbf3cc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('file', sa.Column('post_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'file', 'post', ['post_id'], ['id'])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(None, 'file', type_='foreignkey')
    op.drop_column('file', 'post_id')
