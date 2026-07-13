from datetime import datetime

from pydantic import BaseModel, Field, HttpUrl
from pydantic import ConfigDict


class MovieBase(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str = Field(min_length=10)
    director: str | None = Field(default=None, max_length=150)
    country: str | None = Field(default=None, max_length=100)
    release_year: int = Field(ge=1900)
    duration: int = Field(gt=0)
    age_limit: int = Field(ge=0, le=21)
    rating: float = Field(default=0, ge=0, le=10)
    poster_url: str | None = None
    trailer_url: str | None = None
    is_active: bool = True


class MovieCreate(MovieBase):
    original_title: str | None = None
    genre_id: int


class MovieUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    original_title: str | None = None
    description: str | None = None
    genre_id: int | None = None
    director: str | None = None
    country: str | None = None
    release_year: int | None = Field(default=None, ge=1900)
    duration: int | None = Field(default=None, gt=0)
    age_limit: int | None = None
    rating: float | None = Field(default=None, ge=0, le=10)
    poster_url: str | None = None
    trailer_url: HttpUrl | None = None
    is_active: bool | None = None


class MovieResponse(MovieBase):
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)