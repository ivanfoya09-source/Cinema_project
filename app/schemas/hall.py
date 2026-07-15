from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.hall import HallType


class HallBase(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    hall_type: HallType = HallType.TWO_D
    description: str | None = Field(default=None,max_length=500)
    rows: int = Field(gt=0)
    seats_per_row: int = Field(gt=0)


class HallCreate(HallBase):
    pass


class HallUpdate(BaseModel):
    name: str | None = Field(default=None,min_length=2,max_length=100)
    hall_type: HallType | None = None
    description: str | None = Field(default=None,max_length=500)
    rows: int | None = Field(default=None,gt=0)
    seats_per_row: int | None = Field(default=None,gt=0)


class HallResponse(HallBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)