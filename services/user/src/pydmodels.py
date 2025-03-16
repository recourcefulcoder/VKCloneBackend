from pydantic import BaseModel


class SignUpModel(BaseModel):
    username: str
    email: str
    password: str
