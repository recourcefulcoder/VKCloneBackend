import datetime
from typing import List

from sqlalchemy import DateTime, String, func
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Post(Base):
    __tablename__ = "post"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    author_username: Mapped[str]

    content: Mapped[str] = mapped_column(postgresql.TEXT)

    attached_files: Mapped[List[str]] = mapped_column(postgresql.ARRAY(String))
    # stores names of attached files to access when required

    creation_date: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    last_edit: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
