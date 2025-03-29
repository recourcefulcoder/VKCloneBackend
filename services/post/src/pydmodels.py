from typing import Optional

from pydantic import BaseModel


class PostInfo(BaseModel):
    id: int
    title: str
    author_id: int

    content: str
    creation_date: str
    last_edit: Optional[str] = None
