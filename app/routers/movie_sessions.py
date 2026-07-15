from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_admin
from app.models.user import User
from app.schemas.movie_session import (
    MovieSessionCreate,
    MovieSessionResponse,
    MovieSessionUpdate,
)
from app.services.movie_session_service import MovieSessionService

router = APIRouter(prefix="/sessions",tags=["Movie Sessions"])


@router.get("/",response_model=list[MovieSessionResponse])
def get_sessions(
    db: Session = Depends(get_db),
):
    service = MovieSessionService(db)

    return service.get_all()


@router.get("/{session_id}",response_model=MovieSessionResponse)
def get_session(
    session_id: int,
    db: Session = Depends(get_db),
):
    service = MovieSessionService(db)

    session = service.get_by_id(session_id)

    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Сеанс не знайдено")

    return session


@router.post("/",response_model=MovieSessionResponse,status_code=status.HTTP_201_CREATED)
def create_session(
    data: MovieSessionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    service = MovieSessionService(db)

    return service.create(data)


@router.put("/{session_id}",response_model=MovieSessionResponse)
def update_session(
    session_id: int,
    data: MovieSessionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    service = MovieSessionService(db)

    session = service.get_by_id(session_id)

    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Сеанс не знайдено")

    return service.update(session, data)


@router.delete("/{session_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_session(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    service = MovieSessionService(db)

    session = service.get_by_id(session_id)

    if not session:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Сеанс не знайдено")

    service.delete_session(session)