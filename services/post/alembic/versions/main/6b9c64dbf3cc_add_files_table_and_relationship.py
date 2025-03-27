"""add files table and relationship

Revision ID: 6b9c64dbf3cc
Revises: 867492b55872
Create Date: 2025-03-26 07:44:31.551098

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6b9c64dbf3cc'
down_revision: Union[str, None] = '867492b55872'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('file',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('filename', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('post_file_association_table',
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.Column('file_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['file_id'], ['file.id'], ),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], ),
    sa.PrimaryKeyConstraint('post_id', 'file_id')
    )

    op.add_column("post", sa.Column("author_id", sa.Integer, nullable=False))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('post_file_association_table')
    op.drop_table('file')
    op.drop_column('post', 'author_id')
