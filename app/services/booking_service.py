from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.models.booking import Booking
from app.models.movie_session import MovieSession
from app.models.ticket import Ticket
from app.schemas import ticket
from app.services.reservation_service import ReservationService
from app.services.qr_service import QRService


class BookingService:

    def __init__(self, db: Session):
        self.db = db

    def create_booking(
        self,
        user_id: int,
        session_id: int,
        seats: list[dict],
    ):

        session = (
            self.db.query(MovieSession)
            .filter(MovieSession.id == session_id)
            .first()
        )

        if not session:
            raise ValueError("Сеанс не знайдено")

        if session.available_seats < len(seats):
            raise ValueError("Недостатньо вільних місць")

        total_price = session.price * len(seats)

        try:

            booking = Booking(
                user_id=user_id,
                session_id=session.id,
                total_price=total_price,
            )

            self.db.add(booking)
            self.db.flush()

            for seat in seats:

                exists = (
                    self.db.query(Ticket)
                    .filter(
                        Ticket.session_id == session.id,
                        Ticket.row == seat["row"],
                        Ticket.seat == seat["seat"],
                    )
                    .first()
                )

                if exists:
                    raise ValueError(
                        f"Місце {seat['row']}-{seat['seat']} вже зайняте"
                    )

                ticket = Ticket(
                    booking_id=booking.id,
                    user_id=user_id,
                    session_id=session.id,
                    row=seat["row"],
                    seat=seat["seat"],
                    price=session.price,
                )

                self.db.add(ticket)
                
            session.available_seats -= len(seats)

            self.db.commit()

            for seat in seats:
                ReservationService.release_seat(
                    session.id,
                    seat["row"],
                    seat["seat"],
                )

            self.db.refresh(booking)

            return booking

        except Exception:
            self.db.rollback()
            raise

    def get_occupied_seats(self, session_id: int):

        tickets = (
            self.db.query(Ticket)
            .filter(Ticket.session_id == session_id)
            .all()
        )

        return [
            {
                "row": ticket.row,
                "seat": ticket.seat,
            }
            for ticket in tickets
        ]
    
    def get_booking(self, booking_id: int):

        return (
            self.db.query(Booking)
            .filter(Booking.id == booking_id)
            .first()
        )
    
    def clear_expired_bookings(self):

        expired_bookings = (
            self.db.query(Booking)
            .filter(
                Booking.status == "pending",
                Booking.created_at < datetime.utcnow() - timedelta(minutes=10)
            )
            .all()
        )

        for booking in expired_bookings:

            booking.movie_session.available_seats += len(booking.tickets)

            for ticket in booking.tickets:
                self.db.delete(ticket)

            self.db.delete(booking)

        self.db.commit()