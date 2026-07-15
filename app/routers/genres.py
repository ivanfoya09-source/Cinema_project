from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_admin
from app.models.user import User
from app.schemas.genre import (
    GenreCreate,
    GenreResponse,
)
from app.services.genre_service import GenreService

router = APIRouter(prefix="/genres",tags=["Genres"])


@router.get( "/",response_model=list[GenreResponse])
def get_genres(
    db: Session = Depends(get_db),
):
    service = GenreService(db)

    return service.get_all()


@router.post("/",response_model=GenreResponse,status_code=status.HTTP_201_CREATED)
def create_genre(
    genre: GenreCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    service = GenreService(db)

    return service.create(genre)