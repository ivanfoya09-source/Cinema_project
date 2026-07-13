from sqlalchemy.orm import Session

from app.models import ticket
from app.models import ticket
from app.models.booking import Booking
from app.models.ticket import Ticket
from app.routers.pages import booking
from app.services.qr_service import QRService


class PaymentService:

    def __init__(self, db: Session):
        self.db = db

    def pay_booking(self, booking_id: int):

        booking = (
            self.db.query(Booking)
            .filter(Booking.id == booking_id)
            .first()
        )

        if not booking:
            raise ValueError("Бронювання не знайдено")

        booking.status = "paid"
        booking.payment_status = "paid"
        booking.payment_method = "Card"

        for ticket in booking.tickets:

            ticket.qr_code = QRService.generate(
                f"""
                Ticket #{ticket.id}
                Movie: {booking.movie_session.movie.title}
                Session: {booking.movie_session.id}
                Row: {ticket.row}
                Seat: {ticket.seat}
                """
            )

        ticket.status = "paid"

        self.db.commit()
        self.db.refresh(booking)

        return booking