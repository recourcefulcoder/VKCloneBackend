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
    password: Mapped[str]
    created_date: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    last_login: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    @validates("email")
    def validate_email(self, key, address):
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.fullmatch(pattern, address):
            raise ValueError("Invalid email address!")
        return address

    @validates("password")
    def validate_password(self, key, password):
        pattern = r"""^[A-Za-z0-9!@#$%^&*()_+=\-"'<>,./\\|{}\[\]:;`~]+$"""
        if not re.fullmatch(pattern, password):
            raise ValueError(
                "Invalid password: only "
                "ASCII characters, digits "
                r"""and special symbols !@#$%^&*()_+=\-"'<>,./\|{}[]:;`~"""
                " allowed."
            )
        return password

    @staticmethod
    def hash_password(password: str) -> str:
        pwhash = bcrypt.hashpw(
            password.encode(encoding="utf-8"), bcrypt.gensalt()
        )
        return pwhash.decode(encoding="utf-8")

    def set_password(self, password: str) -> str:
        self.password = self.hash_password(password)
        return str(self.password)
