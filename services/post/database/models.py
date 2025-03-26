import datetime
from typing import List

from sqlalchemy import Column, DateTime, ForeignKey, String, Table, func
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


post_to_file_association_table = Table(
    "post_file_association_table",
    Base.metadata,
    Column("post_id", ForeignKey("post.id"), primary_key=True),
    Column("file_id", ForeignKey("file.id"), primary_key=True),
)


class Post(Base):
    __tablename__ = "post"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    author_id: Mapped[int]

    content: Mapped[str] = mapped_column(postgresql.TEXT)

    files: Mapped[List["File"]] = relationship(
        secondary=post_to_file_association_table, back_populates="posts"
    )
    # stores names of attached files to access when required

    creation_date: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    last_edit: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), nullable=True
    )


class File(Base):
    __tablename__ = "file"
    id: Mapped[int] = mapped_column(primary_key=True)
    filename: Mapped[str]

    posts: Mapped[List[Post]] = relationship(
        secondary=post_to_file_association_table,
        back_populates="files",
    )
