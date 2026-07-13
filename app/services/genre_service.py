from sqlalchemy.orm import Session

from app.models.genre import Genre
from app.schemas.genre import (
    GenreCreate,
    GenreUpdate,
)

from .base_service import BaseService


class GenreService(BaseService):

    def __init__(self, db: Session):
        super().__init__(db)

    def get_all(self):
        return (
            self.db.query(Genre)
            .all()
        )

    def get_by_id(self, genre_id: int):
        return (
            self.db.query(Genre)
            .filter(Genre.id == genre_id)
            .first()
        )

    def create(self, genre: GenreCreate):

        db_genre = Genre(
            name=genre.name,
            description=genre.description,
        )

        return self.add(db_genre)

    def update(
        self,
        db_genre: Genre,
        genre: GenreUpdate,
    ):

        data = genre.model_dump(exclude_unset=True)

        for key, value in data.items():

            if value is None:
                continue

            setattr(db_genre, key, value)

        try:
            self.commit()
            self.refresh(db_genre)

        except Exception:
            self.db.rollback()
            raise

        return db_genre

    def delete_genre(self, db_genre: Genre):
        self.delete(db_genre)