from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.genre import Genre
    from app.models.movie_session import MovieSession


class Movie(Base):
    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(Integer,primary_key=True)
    title: Mapped[str] = mapped_column(String(255),nullable=False)
    original_title: Mapped[str | None] = mapped_column(String(255),nullable=True)
    description: Mapped[str] = mapped_column(Text)
    genre_id: Mapped[int] = mapped_column(ForeignKey("genres.id"),nullable=False)
    director: Mapped[str | None] = mapped_column(String(150),nullable=True)
    country: Mapped[str | None] = mapped_column(String(100),nullable=True)
    release_year: Mapped[int] = mapped_column(Integer)
    duration: Mapped[int] = mapped_column(Integer)
    age_limit: Mapped[int] = mapped_column(Integer)
    rating: Mapped[float] = mapped_column(Float,default=0)
    poster_url: Mapped[str | None] = mapped_column(String(255))
    trailer_url: Mapped[str | None] = mapped_column(String(255),nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean,default=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True),server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True),server_default=func.now(),onupdate=func.now())
    genre: Mapped["Genre"] = relationship(back_populates="movies")
    sessions: Mapped[list["MovieSession"]] = relationship(back_populates="movie",cascade="all, delete-orphan")