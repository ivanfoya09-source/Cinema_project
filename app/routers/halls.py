from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_admin
from app.models.user import User
from app.schemas.hall import (
    HallCreate,
    HallResponse,
    HallUpdate,
)
from app.services.hall_service import HallService

router = APIRouter(prefix="/halls",tags=["Halls"])


@router.get("/",response_model=list[HallResponse])
def get_halls(
    db: Session = Depends(get_db),
):
    service = HallService(db)

    return service.get_all()


@router.get("/{hall_id}",response_model=HallResponse)
def get_hall(
    hall_id: int,
    db: Session = Depends(get_db),
):
    service = HallService(db)

    hall = service.get_by_id(hall_id)

    if not hall:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Зал не знайдено")

    return hall


@router.post("/",response_model=HallResponse,status_code=status.HTTP_201_CREATED)
def create_hall(
    hall: HallCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    service = HallService(db)

    return service.create(hall)


@router.put("/{hall_id}",response_model=HallResponse)
def update_hall(
    hall_id: int,
    hall: HallUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    service = HallService(db)

    db_hall = service.get_by_id(hall_id)

    if not db_hall:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Зал не знайдено")

    return service.update(db_hall, hall)


@router.delete("/{hall_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_hall(
    hall_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin),
):
    service = HallService(db)

    hall = service.get_by_id(hall_id)

    if not hall:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Зал не знайдено")

    service.delete_hall(hall)