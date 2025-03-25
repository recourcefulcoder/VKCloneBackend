from typing import Optional

from pydantic import BaseModel


class PostInfo(BaseModel):
    id: Optional[int] = None
    title: Optional[str] = None
    content: Optional[str] = None
    author_username: Optional[str] = None
    creation_date: Optional[str] = None
