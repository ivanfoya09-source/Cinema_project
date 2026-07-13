from pydantic import BaseModel, ConfigDict, Field
from typing import List
from datetime import datetime


class SeatCreate(BaseModel):
    row: int = Field(gt=0)
    seat: int = Field(gt=0)


class BookingCreate(BaseModel):
    session_id: int = Field(gt=0)
    seats: List[SeatCreate] = Field(min_length=1)


class TicketResponse(BaseModel):
    id: int
    row: int
    seat: int
    price: float

    model_config = ConfigDict(from_attributes=True)


class BookingResponse(BaseModel):
    id: int
    user_id: int
    session_id: int
    total_price: float
    status: str
    payment_status: str
    payment_method: str | None = None
    created_at: datetime
    tickets: List[TicketResponse]

    model_config = ConfigDict(from_attributes=True)