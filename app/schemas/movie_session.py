from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator


class MovieSessionBase(BaseModel):
    movie_id: int = Field(gt=0)
    hall_id: int = Field(gt=0)
    start_time: datetime
    end_time: datetime
    language: str = Field(
    default="Українська",
    max_length=50,
)
    subtitle: bool = False
    price: float = Field(gt=0)
    available_seats: int = Field(ge=0)
    format: str = Field(
    default="2D",
    max_length=20,
)
    is_active: bool = True

    @model_validator(mode="after")
    def validate_time(self):
        if self.end_time <= self.start_time:
            raise ValueError("Час завершення повинен бути пізніше часу початку")
        return self


class MovieSessionCreate(MovieSessionBase):
    pass


class MovieSessionUpdate(BaseModel):
    movie_id: int | None = Field(default=None, gt=0)
    hall_id: int | None = Field(default=None, gt=0)
    start_time: datetime | None = None
    end_time: datetime | None = None
    language: str | None = Field(default=None, max_length=50)
    subtitle: bool | None = None
    price: float | None = Field(default=None, gt=0)
    available_seats: int | None = Field(default=None, ge=0)
    format: str | None = Field(default=None, max_length=20)
    is_active: bool | None = None


class MovieSessionResponse(MovieSessionBase):
    id: int

    model_config = ConfigDict(from_attributes=True)