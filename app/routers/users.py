from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_admin, get_current_user
from app.models.user import User
from app.schemas.user import (
    UserCreate,
    UserResponse,
    UserUpdate,
)
from app.services.user_service import UserService


router = APIRouter( prefix="/users",tags=["Users"])


@router.get("/",response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):

    service = UserService(db)
    return service.get_all()


@router.get("/{user_id}",response_model=UserResponse)
def get_user(user_id: int,db: Session = Depends(get_db)):

    user = UserService(db).get_by_id(user_id)

    if not user:
        raise HTTPException(status_code=404,detail="Користувача не знайдено")

    return user


@router.post("/",response_model=UserResponse,status_code=201)
def create_user(user: UserCreate,db: Session = Depends(get_db)):
    return UserService(db).create(user)


@router.put("/me", response_model=UserResponse)
def update_profile(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = UserService(db)

    user = service.get_by_id(current_user.id)

    return service.update(
        user,
        user_data.model_dump(exclude_unset=True)
    )