from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import decode_token
from app.models.user import User
from fastapi import Request
from fastapi.responses import RedirectResponse


def get_current_user(request: Request,db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(status_code=401,detail="Необхідно увійти")

    payload = decode_token(token)

    if payload is None:
        raise HTTPException(status_code=401,detail="Недійсний токен")

    user_id = payload.get("sub")

    if user_id is None:
        raise HTTPException(status_code=401,detail="Недійсний токен")

    user = (db.query(User).filter(User.id == int(user_id)).first())

    if user is None:
        raise HTTPException(status_code=401,detail="Користувача не знайдено")

    return user


def get_current_user_optional(request: Request,db: Session = Depends(get_db)):
    token = request.cookies.get("access_token")

    if not token:
        return None

    payload = decode_token(token)

    if payload is None:
        return None

    user_id = payload.get("sub")

    if not user_id:
        return None

    return (db.query(User).filter(User.id == int(user_id)).first())


def get_current_admin(current_user: User = Depends(get_current_user)):

    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Доступ заборонено")

    return current_user

def login_required(request: Request):
    token = request.cookies.get("access_token")

    if not token:
        return RedirectResponse("/login", status_code=302)

    return None