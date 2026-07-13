from sqlalchemy.orm import Session

from app.models.hall import Hall
from app.schemas.hall import (
    HallCreate,
    HallUpdate,
)

from .base_service import BaseService


class HallService(BaseService):

    def __init__(self, db: Session):
        super().__init__(db)

    def get_all(self):
        return self.db.query(Hall).all()

    def get_by_id(self, hall_id: int):
        return (
            self.db.query(Hall)
            .filter(Hall.id == hall_id)
            .first()
        )

    def create(self, hall: HallCreate):

        db_hall = Hall(
            name=hall.name,
            hall_type=hall.hall_type,
            description=hall.description,
            rows=hall.rows,
            seats_per_row=hall.seats_per_row,
        )

        return self.add(db_hall)

    def update(
        self,
        db_hall: Hall,
        hall: HallUpdate,
    ):

        data = hall.model_dump(exclude_unset=True)

        for key, value in data.items():

            if value is None:
                continue

            setattr(db_hall, key, value)

        try:
            self.commit()
            self.refresh(db_hall)

        except Exception:
            self.db.rollback()
            raise

        return db_hall

    def delete_hall(self, db_hall: Hall):
        self.delete(db_hall)