from datetime import date
from typing import List, Optional

from pydantic import BaseModel


class MovieBase(BaseModel):
    name: str
    date: date
    score: float
    genre: str
    overview: str
    crew: list
    orig_title: str
    status: str
    orig_lang: str
    budget: float
    revenue: float
    country: str


class MovieCreate(MovieBase):
    pass


class MovieDetailResponseSchema(MovieBase):
    id: int

    class Config:
        from_attributes = True


class MovieListResponseSchema(BaseModel):
    movies: List[MovieDetailResponseSchema]
    prev_page: Optional[int]
    next_page: Optional[int]
    total_pages: int
    total_items: int
