from sqlalchemy.orm import Session

from app.models.ticket import Ticket
from app.schemas.ticket import (
    TicketCreate,
    TicketUpdate,
)

from .base_service import BaseService


class TicketService(BaseService):

    def __init__(self, db: Session):
        super().__init__(db)

    def get_all(self):
        return self.db.query(Ticket).all()

    def get_by_id(self, ticket_id: int):
        return (
            self.db.query(Ticket)
            .filter(Ticket.id == ticket_id)
            .first()
        )

    def get_by_booking(self, booking_id: int):
        return (
            self.db.query(Ticket)
            .filter(Ticket.booking_id == booking_id)
            .all()
        )

    def get_by_user(self, user_id: int):
        return (
            self.db.query(Ticket)
            .filter(Ticket.user_id == user_id)
            .all()
        )

    def create(self, ticket: TicketCreate):

        db_ticket = Ticket(
            booking_id=ticket.booking_id,
            session_id=ticket.session_id,
            row=ticket.row,
            seat=ticket.seat,
            price=ticket.price,
            status=ticket.status,
            qr_code=ticket.qr_code,
        )

        return self.add(db_ticket)

    def update(self,db_ticket: Ticket,ticket: TicketUpdate):

        data = ticket.model_dump(exclude_unset=True)

        for key, value in data.items():

            if value is None:
                continue

            setattr(db_ticket, key, value)

        try:
            self.commit()
            self.refresh(db_ticket)

        except Exception:
            self.db.rollback()
            raise

        return db_ticket

    def delete_ticket(self, ticket: Ticket):
        self.delete(ticket)