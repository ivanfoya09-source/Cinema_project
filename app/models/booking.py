from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import (
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.ticket import Ticket
    from app.models.movie_session import MovieSession


class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(Integer,primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"),nullable=False)
    status: Mapped[str] = mapped_column(String(30),default="pending")
    total_price: Mapped[float] = mapped_column(Float,default=0)
    payment_status: Mapped[str] = mapped_column(String(30),default="pending")
    payment_method: Mapped[str | None] = mapped_column(String(50),nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True),server_default=func.now())
    user: Mapped["User"] = relationship(back_populates="bookings")
    tickets: Mapped[list["Ticket"]] = relationship(back_populates="booking",cascade="all, delete-orphan")
    session_id: Mapped[int] = mapped_column(ForeignKey("movie_sessions.id"),nullable=False)
    movie_session: Mapped["MovieSession"] = relationship(back_populates="bookings")