import datetime
import re

import bcrypt

from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, validates
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    _password: Mapped[str] = mapped_column("password")
    created_date: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    last_login: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        if "password" in kwargs.keys():
            self.password = kwargs["password"]

    @validates("email")
    def validate_email(self, key, address):
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.fullmatch(pattern, address):
            raise ValueError("Invalid email address!")
        return address

    @staticmethod
    def hash_password(password: str) -> str:
        pwhash = bcrypt.hashpw(
            password.encode(encoding="utf-8"), bcrypt.gensalt()
        )
        return pwhash.decode(encoding="utf-8")

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password: str):
        self._password = self.hash_password(password)

    def verify_password(self, password: str):
        encoded = password.encode("utf-8")
        return bcrypt.checkpw(encoded, self.password.encode("utf-8"))
