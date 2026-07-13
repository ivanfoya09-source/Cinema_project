from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_admin
from app.models.movie import Movie
from app.models.user import User
from app.schemas.movie import MovieCreate
from app.services.movie_service import MovieService
from app.schemas.genre import GenreCreate
from app.services.genre_service import GenreService
from app.schemas.hall import HallCreate
from app.services.hall_service import HallService


router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)


@router.post(
    "/movies",
    status_code=status.HTTP_201_CREATED,
)
def create_movie(
    movie: MovieCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    return MovieService(db).create(movie)


@router.delete(
    "/movies/{movie_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_movie(
    movie_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    service = MovieService(db)

    movie = service.get_by_id(movie_id)

    if movie is None:
        raise HTTPException(
            status_code=404,
            detail="Фільм не знайдено",
        )

    service.delete_movie(movie)


@router.post(
    "/genres",
    status_code=status.HTTP_201_CREATED,
)
def create_genre(
    genre: GenreCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    service = GenreService(db)

    return service.create(genre)


@router.post(
    "/halls",
    status_code=status.HTTP_201_CREATED,
)
def create_hall(
    hall: HallCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    service = HallService(db)

    return service.create(hall)

@router.get("/movies/{movie_id}")
def get_movie(
    movie_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    service = MovieService(db)

    movie = service.get_by_id(movie_id)

    if not movie:
        raise HTTPException(
            status_code=404,
            detail="Фільм не знайдено",
        )

    return movie

@router.put(
    "/movies/{movie_id}",
    status_code=status.HTTP_200_OK,
)
def update_movie(
    movie_id: int,
    movie_data: MovieCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    service = MovieService(db)

    movie = service.get_by_id(movie_id)

    if not movie:
        raise HTTPException(
            status_code=404,
            detail="Фільм не знайдено",
        )

    return service.update(movie, movie_data)