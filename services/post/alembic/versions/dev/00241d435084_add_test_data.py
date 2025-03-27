"""add_test_data

Revision ID: 00241d435084
Revises: 
Create Date: 2025-03-27 09:22:58.243073

"""
import datetime
import sys
from typing import Sequence, Union

from database.models import Post, File

import settings

from alembic import op
import sqlalchemy as sa

from sqlalchemy.sql import table, column


# revision identifiers, used by Alembic.
revision: str = '00241d435084'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = ('dev',)
depends_on: Union[str, Sequence[str], None] = 'main'


post_tn = Post.__tablename__
file_tn = File.__tablename__


def upgrade() -> None:
    """Upgrade schema."""
    if not settings.DEBUG or settings.TESTING:
        print("Invalid environment configuration: "
              "POST_DEBUG environment variable is set to False or "
              "POST_TESTING env var is set to True. \nAborting...")
        sys.exit(1)
    post = table(
        post_tn,
        column("id", sa.Integer),
        column("author_id", sa.Integer),
        column("title", sa.String),
        column("content", sa.Text),
        column("creation_date", sa.DateTime),
        column("last_edit", sa.DateTime),
    )
    op.bulk_insert(
        post,
        [
            {
                "id": 1,
                "author_id": 1,
                "title": "Cute intro UwU",
                "content": "<p>Hi everyoneeeee ^_^</p>",
                "creation_date": datetime.datetime(
                    year=2012, month=4, day=13, hour=13, minute=29, second=13
                ),
            },
            {
                "id": 2,
                "author_id": 1,
                "title": "Hehehehehe",
                "content": "<p>I'm about to give you some "
                           "jokes my seeties! Listen closely: "
                           "заходит как-то улитка в бар...</p>",
                "creation_date": datetime.datetime(
                    year=2012, month=4, day=14, hour=13, minute=29, second=13
                ),
            },
        ]
    )
    op.execute(
        f"SELECT setval('{post_tn}_id_seq', 2);"
    )


def downgrade() -> None:
    """Downgrade schema."""
    if not settings.DEBUG or settings.TESTING:
        print("Invalid environment configuration: "
              "POST_DEBUG environment variable is set to False or "
              "POST_TESTING env var is set to True. \nAborting...")
        sys.exit(1)
    op.execute(
        f"DELETE FROM public.{post_tn} WHERE id IN (1, 2)"
    )
    op.execute(
        f"SELECT setval('{post_tn}_id_seq', (SELECT MAX(id) FROM public.{post_tn}));"
    )
