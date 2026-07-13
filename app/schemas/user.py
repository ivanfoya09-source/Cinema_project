from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field, HttpUrl


class UserBase(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    first_name: str | None = None
    last_name: str | None = None
    phone: str | None = Field(
    default=None,
    max_length=20,
)
    birth_date: date | None = None
    city: str | None = None
    avatar: HttpUrl | None = None


class UserCreate(UserBase):
    password: str = Field(min_length=8)


class UserUpdate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr | None = None
    first_name: str | None = None
    last_name: str | None = None
    phone: str | None = Field(
    default=None,
    max_length=20,
)
    birth_date: date | None = None
    city: str | None = None
    avatar: HttpUrl | None = None


class UserResponse(UserBase):
    id: int
    role: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)