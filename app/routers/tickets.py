from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_admin
from app.models.user import User
from app.schemas.ticket import (
    TicketCreate,
    TicketResponse,
)
from app.services.ticket_service import TicketService

router = APIRouter(prefix="/tickets",tags=["Tickets"])


@router.get("/",response_model=list[TicketResponse])
def get_tickets(
    db: Session = Depends(get_db),
):
    service = TicketService(db)

    return service.get_all()


@router.get("/{ticket_id}",response_model=TicketResponse)
def get_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
):
    service = TicketService(db)

    ticket = service.get_by_id(ticket_id)

    if not ticket:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Квиток не знайдено")

    return ticket


@router.post("/",response_model=TicketResponse,status_code=status.HTTP_201_CREATED)
def create_ticket(
    ticket: TicketCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    service = TicketService(db)

    return service.create(ticket)


@router.delete("/{ticket_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    service = TicketService(db)

    ticket = service.get_by_id(ticket_id)

    if not ticket:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Квиток не знайдено")

    service.delete_ticket(ticket)