"""add test data

Revision ID: 47064c241be8
Revises: 
Create Date: 2025-03-17 12:03:46.166354

"""
from typing import Sequence, Union

from alembic import op

from database.models import User

from sqlalchemy import String, Integer
from sqlalchemy.sql import table, column


# revision identifiers, used by Alembic.
revision: str = '47064c241be8'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = ('test',)
depends_on: Union[str, Sequence[str], None] = "84c5ba7d03b3"


user_tn = User.__tablename__


def upgrade() -> None:
    """Upgrade schema."""
    user = table(
        user_tn,
        column("id", Integer),
        column("username", String),
        column("email", String),
        column("password", String),
    )
    op.bulk_insert(
        user,
        [
            {
                "id": 1,
                "username": "kiric",
                "email": "valid@gmail.com",
                "password": User.hash_password("Harmonica52"),
            },
            {
                "id": 2,
                "username": "mimic",
                "email": "valid2@gmail.com",
                "password": User.hash_password("Harmonica52"),
            }
        ]
    )
    op.execute(
        f"SELECT setval('{user_tn}_id_seq', 2);"
    )


def downgrade() -> None:
    op.execute(
        f"DELETE FROM public.{user_tn} WHERE id IN (1, 2)"
    )
    op.execute(
        f"SELECT setval('{user_tn}_id_seq', (SELECT MAX(id) FROM public.{user_tn}));"
    )
