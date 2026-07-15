from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.payment_service import PaymentService
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request

from app.models.booking import Booking


templates = Jinja2Templates(directory="app/templates")

router = APIRouter(prefix="/payment",tags=["Payment"])


@router.post("/{booking_id}")
def pay_booking(
    booking_id: int,
    db: Session = Depends(get_db),
):

    service = PaymentService(db)

    try:

        booking = service.pay_booking(booking_id)

        return {
            "message": "Оплата успішна",
            "booking_id": booking.id,
        }

    except ValueError as e:

        raise HTTPException(status_code=404,detail=str(e))
    

@router.get("/{booking_id}", response_class=HTMLResponse)
def payment_page(
    request: Request,
    booking_id: int,
    db: Session = Depends(get_db),
):

    booking = (
        db.query(Booking)
        .filter(Booking.id == booking_id)
        .first()
    )

    if not booking:
        raise HTTPException(status_code=404,detail="Бронювання не знайдено")

    return templates.TemplateResponse(
        "payment.html",
        {
            "request": request,
            "booking": booking,
        },
    )

    
@router.get("/ticket/{booking_id}", response_class=HTMLResponse)
def ticket_page(
    request: Request,
    booking_id: int,
    db: Session = Depends(get_db),
):

    booking = (
        db.query(Booking)
        .filter(Booking.id == booking_id)
        .first()
    )

    if not booking:
        raise HTTPException(status_code=404,detail="Бронювання не знайдено")

    return templates.TemplateResponse(
        "ticket.html",
        {
            "request": request,
            "booking": booking,
        },
    )