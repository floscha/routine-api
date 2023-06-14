from typing import Optional

from pydantic import BaseModel


class BlockDTO(BaseModel):
    id: str
    type: str
    content: str


class NotesDTO(BaseModel):
    blocks: list[BlockDTO]


class PageDTO(BaseModel):
    title: str
    id: Optional[str]
    created: Optional[str]
    notes: Optional[NotesDTO]
    parent: Optional[str]


class Page(PageDTO):
    def __str__(self) -> str:
        return f"Page(title: {self.title!r})"
