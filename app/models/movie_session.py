from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.movie import Movie
    from app.models.hall import Hall
    from app.models.ticket import Ticket
    from app.models.booking import Booking


class MovieSession(Base):
    __tablename__ = "movie_sessions"

    id: Mapped[int] = mapped_column(Integer,primary_key=True)
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"),nullable=False)
    hall_id: Mapped[int] = mapped_column(ForeignKey("halls.id"),nullable=False)
    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    end_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    language: Mapped[str] = mapped_column(String(50),default="Українська")
    subtitle: Mapped[bool] = mapped_column(Boolean,default=False)
    price: Mapped[float] = mapped_column(Float,default=0)
    available_seats: Mapped[int] = mapped_column(Integer,default=0)
    format: Mapped[str] = mapped_column(String(20),default="2D")
    is_active: Mapped[bool] = mapped_column(Boolean,default=True)
    movie: Mapped["Movie"] = relationship(back_populates="sessions")
    hall: Mapped["Hall"] = relationship(back_populates="sessions")
    tickets: Mapped[list["Ticket"]] = relationship(back_populates="movie_session",cascade="all, delete-orphan")
    bookings: Mapped[list["Booking"]] = relationship(back_populates="movie_session",cascade="all, delete-orphan")