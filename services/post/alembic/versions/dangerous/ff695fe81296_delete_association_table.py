"""delete association table

Revision ID: ff695fe81296
Revises: cabdac6d0430
Create Date: 2025-03-27 14:03:10.402622

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ff695fe81296'
down_revision: Union[str, None] = 'cabdac6d0430'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = 'bf9d6510c468'


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_constraint(
        'post_file_association_table_file_id_fkey',
        'post_file_association_table',
        type_='foreignkey'
    )
    op.drop_constraint(
        'post_file_association_table_post_id_fkey',
        'post_file_association_table',
        type_='foreignkey')
    op.drop_table('post_file_association_table')


def downgrade() -> None:
    """Downgrade schema."""
    op.create_table(
        'post_file_association_table',
        sa.Column('post_id', sa.Integer(), nullable=False),
        sa.Column('file_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['file_id'], ['file.id'], ),
        sa.ForeignKeyConstraint(['post_id'], ['post.id'], ),
        sa.PrimaryKeyConstraint('post_id', 'file_id')
    )
