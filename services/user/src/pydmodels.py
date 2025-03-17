import re

from pydantic import BaseModel, field_validator


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
