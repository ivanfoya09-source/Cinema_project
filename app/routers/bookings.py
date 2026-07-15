from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.booking import (
    BookingCreate,
    BookingResponse,
)
from app.services.booking_service import BookingService


router = APIRouter(prefix="/bookings",tags=["Bookings"])


@router.post("/",response_model=BookingResponse,status_code=status.HTTP_201_CREATED)
def create_booking(
    booking: BookingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = BookingService(db)

    try:
        return service.create_booking(
            user_id=current_user.id,
            session_id=booking.session_id,
            seats=[
                {
                    "row": seat.row,
                    "seat": seat.seat,
                }
                for seat in booking.seats
            ],
        )

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))



@router.get("/session/{session_id}")
def occupied_seats(
    session_id: int,
    db: Session = Depends(get_db),
):
    service = BookingService(db)

    return service.get_occupied_seats(session_id)