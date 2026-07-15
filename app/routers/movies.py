from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_admin
from app.models.user import User
from app.schemas.movie import (
    MovieCreate,
    MovieResponse,
    MovieUpdate,
)
from app.services.movie_service import MovieService

router = APIRouter(prefix="/movies",tags=["Movies"])


@router.get("/",response_model=list[MovieResponse])
def get_movies(
    db: Session = Depends(get_db),
):
    service = MovieService(db)

    return service.get_all()


@router.get("/{movie_id}",response_model=MovieResponse)
def get_movie(
    movie_id: int,
    db: Session = Depends(get_db),
):
    service = MovieService(db)

    movie = service.get_by_id(movie_id)

    if not movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Фільм не знайдено")

    return movie


@router.post("/",response_model=MovieResponse,status_code=status.HTTP_201_CREATED)
def create_movie(
    movie: MovieCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    service = MovieService(db)

    return service.create(movie)


@router.put("/{movie_id}",response_model=MovieResponse)
def update_movie(
    movie_id: int,
    movie: MovieUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    service = MovieService(db)

    db_movie = service.get_by_id(movie_id)

    if not db_movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Фільм не знайдено")

    return service.update(db_movie, movie)


@router.delete("/{movie_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_movie(
    movie_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    service = MovieService(db)

    movie = service.get_by_id(movie_id)

    if not movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Фільм не знайдено")

    service.delete_movie(movie)