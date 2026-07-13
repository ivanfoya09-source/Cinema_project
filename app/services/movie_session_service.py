from sqlalchemy.orm import Session

from app.models.movie_session import MovieSession
from app.schemas.movie_session import (
    MovieSessionCreate,
    MovieSessionUpdate,
)

from .base_service import BaseService


class MovieSessionService(BaseService):

    def __init__(self, db: Session):
        super().__init__(db)

    def get_all(self):
        return self.db.query(MovieSession).all()

    def get_by_id(self, session_id: int):
        return (
            self.db.query(MovieSession)
            .filter(MovieSession.id == session_id)
            .first()
        )

    def create(self, session: MovieSessionCreate):

        db_session = MovieSession(
            movie_id=session.movie_id,
            hall_id=session.hall_id,
            start_time=session.start_time,
            end_time=session.end_time,
            language=session.language,
            subtitle=session.subtitle,
            price=session.price,
            available_seats=session.available_seats,
            format=session.format,
            is_active=session.is_active,
        )

        return self.add(db_session)

    def update(
        self,
        db_session: MovieSession,
        session: MovieSessionUpdate,
    ):

        data = session.model_dump(exclude_unset=True)

        for key, value in data.items():

            if value is None:
                continue

            setattr(db_session, key, value)

        try:
            self.commit()
            self.refresh(db_session)

        except Exception:
            self.db.rollback()
            raise

        return db_session

    def delete_session(self, db_session: MovieSession):
        self.delete(db_session)

    def get_by_movie(self, movie_id: int):
        return (
            self.db.query(MovieSession)
            .filter(
                MovieSession.movie_id == movie_id,
                MovieSession.is_active == True,
            )
            .all()
        )

    def get_active(self):
        return (
            self.db.query(MovieSession)
            .filter(MovieSession.is_active == True)
            .all()
        )

    def get_upcoming(self):
        from datetime import datetime

        return (
            self.db.query(MovieSession)
            .filter(
                MovieSession.start_time >= datetime.now(),
                MovieSession.is_active == True,
            )
            .order_by(MovieSession.start_time)
            .all()
        )