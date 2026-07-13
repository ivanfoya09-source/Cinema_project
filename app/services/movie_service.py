from sqlalchemy.orm import Session
import json

from app.core.redis import redis_client
from app.models.movie import Movie
from app.schemas.movie import MovieCreate, MovieUpdate

from .base_service import BaseService


class MovieService(BaseService):

    CACHE_KEY = "movies"

    def __init__(self, db: Session):
        super().__init__(db)

    def get_all(
    self,
    skip: int = 0,
    limit: int = 6,
    ):
        return (
        self.db.query(Movie)
        .offset(skip)
        .limit(limit)
        .all()
    )
    def count(self):
        return self.db.query(Movie).count()

    def get_by_id(self, movie_id: int):
        return (
            self.db.query(Movie)
            .filter(Movie.id == movie_id)
            .first()
        )

    def create(self, movie: MovieCreate):

        db_movie = Movie(
            title=movie.title,
            original_title=movie.original_title,
            description=movie.description,
            genre_id=movie.genre_id,
            director=movie.director,
            country=movie.country,
            release_year=movie.release_year,
            duration=movie.duration,
            age_limit=movie.age_limit,
            rating=movie.rating,
            poster_url=movie.poster_url,
            trailer_url=movie.trailer_url,
            is_active=movie.is_active,
        )

        db_movie = self.add(db_movie)

        redis_client.delete(self.CACHE_KEY)

        return db_movie

    def update(
        self,
        db_movie: Movie,
        movie: MovieUpdate,
    ):

        data = movie.model_dump(exclude_unset=True)

        for key, value in data.items():

            if value is None:
                continue

            setattr(db_movie, key, value)

        try:
            self.commit()
            self.refresh(db_movie)

            redis_client.delete(self.CACHE_KEY)

        except Exception:
            self.db.rollback()
            raise

        return db_movie

    def delete_movie(self, db_movie: Movie):

        self.delete(db_movie)

        redis_client.delete(self.CACHE_KEY)

    def search(self, title: str):
        return (
            self.db.query(Movie)
            .filter(Movie.title.ilike(f"%{title}%"))
            .all()
        )

    def get_active(self):
        return (
            self.db.query(Movie)
            .filter(Movie.is_active == True)
            .all()
        )