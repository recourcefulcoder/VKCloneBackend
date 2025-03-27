"""table creation

Revision ID: 867492b55872
Revises: 
Create Date: 2025-03-25 13:33:49.376955

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '867492b55872'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = ('main',)
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('author_username', sa.String(), nullable=False),
    sa.Column('content', sa.TEXT(), nullable=False),
    sa.Column('attached_files', postgresql.ARRAY(sa.String()), nullable=False),
    sa.Column('creation_date', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('last_edit', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('post')
