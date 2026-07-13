from pydantic import BaseModel


class Seat(BaseModel):
    row: int
    seat: int


class ReservationRequest(BaseModel):
    session_id: int
    seats: list[Seat]


class ReservationResponse(BaseModel):
    message: str