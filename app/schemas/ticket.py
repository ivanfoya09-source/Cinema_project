from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.ticket import TicketStatus


class TicketBase(BaseModel):
    booking_id: int = Field(gt=0)
    session_id: int = Field(gt=0)
    row: int = Field(gt=0)
    seat: int = Field(gt=0)
    price: float = Field(gt=0)
    status: TicketStatus = TicketStatus.RESERVED

    qr_code: str | None = Field(default=None, max_length=255)


class TicketCreate(TicketBase):
    pass


class TicketUpdate(BaseModel):
    status: TicketStatus | None = Field(default=None)
    qr_code: str | None = Field(default=None, max_length=255)


class TicketResponse(TicketBase):
    id: int
    booked_at: datetime

    model_config = ConfigDict(from_attributes=True)