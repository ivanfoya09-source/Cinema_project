from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy import Enum

from app.core.database import Base

import enum

if TYPE_CHECKING:
    from app.models.booking import Booking
    from app.models.movie_session import MovieSession
    from app.models.user import User


class TicketStatus(str, enum.Enum):
    RESERVED = "reserved"
    PAID = "paid"
    USED = "used"
    CANCELLED = "cancelled"


class Ticket(Base):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(Integer,primary_key=True)
    booking_id: Mapped[int] = mapped_column(ForeignKey("bookings.id"),nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"),nullable=False)
    session_id: Mapped[int] = mapped_column(ForeignKey("movie_sessions.id"),nullable=False)
    row: Mapped[int] = mapped_column(Integer)
    seat: Mapped[int] = mapped_column(Integer)
    price: Mapped[float] = mapped_column(Float,default=0)
    status: Mapped[TicketStatus] = mapped_column(Enum(TicketStatus),default=TicketStatus.RESERVED)
    qr_code: Mapped[str | None] = mapped_column(String(255),nullable=True)
    booked_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True),server_default=func.now())
    booking: Mapped["Booking"] = relationship(back_populates="tickets")
    user: Mapped["User"] = relationship(back_populates="tickets")
    movie_session: Mapped["MovieSession"] = relationship(back_populates="tickets")