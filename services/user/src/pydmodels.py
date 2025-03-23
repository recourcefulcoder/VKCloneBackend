import datetime
import re
from typing import Optional

from pydantic import BaseModel, field_validator, model_validator


class SignUpModel(BaseModel):
    username: str
    email: str
    password: str

    @field_validator("email")
    @classmethod
    def validate_email(cls, email: str):
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.fullmatch(pattern, email):
            raise ValueError("Invalid email address!")
        return email

    @field_validator("password")
    @classmethod
    def validate_password(cls, password: str):
        pattern = r"""^[A-Za-z0-9!@#$%^&*()_+?=\-"'<>,./\\|{}\[\]:;`~ ]+$"""
        if not re.fullmatch(pattern, password):
            raise ValueError(
                "Invalid password: only "
                "ASCII characters, digits "
                r"""and special symbols !@#$%^&*()_+?=\-"'<>,./\|{}[]:;`~"""
                "AND <space symbol> allowed."
            )
        return password


class LoginModel(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: str

    @model_validator(mode="after")
    def check_sub(self):
        both_missed = not (self.email is not None or self.username is not None)
        both_provided = self.email is not None and self.username is not None
        if both_missed or both_provided:
            raise ValueError(
                "Whether email or username must be provided: "
                "both/not one is invalid"
            )
        return self


class RefreshToken(BaseModel):
    refresh_token: str


class UserInfo(BaseModel):
    id: int
    username: str
    email: str
    created_date: datetime.datetime


class UserUpdate(BaseModel):
    password: Optional[str] = None
    username: Optional[str] = None
    email: Optional[str] = None
