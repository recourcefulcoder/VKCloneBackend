import datetime
from typing import List

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Post(Base):
    __tablename__ = "post"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    author_id: Mapped[int]

    content: Mapped[str] = mapped_column(postgresql.TEXT)

    creation_date: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    last_edit: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    files: Mapped[List["File"]] = relationship(back_populates="post")


class File(Base):
    __tablename__ = "file"
    id: Mapped[int] = mapped_column(primary_key=True)
    filename: Mapped[str]
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))

    post: Mapped[Post] = relationship(
        back_populates="files",
    )
