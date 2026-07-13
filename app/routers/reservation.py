from fastapi import APIRouter, Depends, HTTPException

from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.reservation import (
    ReservationRequest,
    ReservationResponse,
)
from app.services.reservation_service import ReservationService

router = APIRouter(
    prefix="/reservations",
    tags=["Reservations"],
)


@router.post(
    "/",
    response_model=ReservationResponse,
)
def reserve_seats(
    data: ReservationRequest,
    current_user: User = Depends(get_current_user),
):

    for seat in data.seats:

        success = ReservationService.reserve_seat(
            data.session_id,
            seat.row,
            seat.seat,
        )

        if not success:
            raise HTTPException(
                status_code=409,
                detail=f"Місце {seat.row}-{seat.seat} вже зарезервоване",
            )

    return {
        "message": "Місця успішно зарезервовано на 10 хвилин"
    }