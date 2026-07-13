from urllib import response

from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.auth import LoginRequest, RegisterRequest, Token
from app.schemas.user import UserResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth",tags=["Authentication"])


@router.post("/register",response_model=UserResponse,status_code=status.HTTP_201_CREATED)
def register(user: RegisterRequest,db: Session = Depends(get_db)):
    service = AuthService(db)

    try:
        return service.register(user)

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login",response_model=Token)
def login(
    response: Response,
    data: LoginRequest,
    db: Session = Depends(get_db),
):
    service = AuthService(db)

    tokens = service.login(data)

    if not tokens:
        raise HTTPException(
            status_code=401,
            detail="Невірний email або пароль",
        )

    response.set_cookie(
    key="access_token",
    value=tokens["access_token"],
    httponly=True,
    samesite="lax",
    secure=False,      # True після переходу на HTTPS
    max_age=60 * 60,
    )

    response.set_cookie(
    key="refresh_token",
    value=tokens["refresh_token"],
    httponly=True,
    samesite="lax",
    secure=False,
    max_age=60 * 60 * 24 * 7,
    )

    return tokens


@router.post("/logout")
def logout(response: Response):

    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")

    return {
        "message": "Вихід виконано успішно"
    }