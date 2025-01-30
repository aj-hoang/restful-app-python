import uuid

from sqlmodel import SQLModel, Field
from typing import Optional


class MovieBase(SQLModel):
    movie: str = Field(max_length=255)
    genre: str = Field(max_length=255)


class MovieCreate(MovieBase):
    pass


class MovieUpdate(MovieBase):
    pass


# DB table
class Movie(MovieBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    movie: str
    genre: str
