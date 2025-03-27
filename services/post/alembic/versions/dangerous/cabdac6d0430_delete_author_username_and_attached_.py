"""delete author_username and attached_files collumn

Revision ID: cabdac6d0430
Revises: 
Create Date: 2025-03-26 09:11:24.133844

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cabdac6d0430'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = ('dangerous',)
depends_on: Union[str, Sequence[str], None] = '6b9c64dbf3cc'


def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table("post") as batch_op:
        batch_op.drop_column("author_username")
        batch_op.drop_column("attached_files")


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column("post", sa.Column("author_username", sa.String, nullable=False))
    op.add_column("post", sa.Column(
        "attached_files", sa.dialects.postgresql.ARRAY(sa.String), nullable=False
    ))
