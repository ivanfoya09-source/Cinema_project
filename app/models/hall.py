from __future__ import annotations

import enum
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime
from sqlalchemy import Enum
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.movie_session import MovieSession


class HallType(str, enum.Enum):
    TWO_D = "2D"
    THREE_D = "3D"
    IMAX = "IMAX"
    FOUR_DX = "4DX"


class Hall(Base):
    __tablename__ = "halls"

    id: Mapped[int] = mapped_column(Integer,primary_key=True,index=True)
    name: Mapped[str] = mapped_column(String(100),unique=True,nullable=False)
    hall_type: Mapped[HallType] = mapped_column(Enum(HallType),default=HallType.TWO_D,nullable=False)
    description: Mapped[str | None] = mapped_column(String(255),nullable=True)
    rows: Mapped[int] = mapped_column(Integer,nullable=False)
    seats_per_row: Mapped[int] = mapped_column(Integer,nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean,default=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True),server_default=func.now())
    sessions: Mapped[list["MovieSession"]] = relationship(back_populates="hall",cascade="all, delete-orphan")