from sqlalchemy.orm import Session

from app.core.security import (
    verify_password,
    hash_password,
    create_access_token,
    create_refresh_token,
)

from app.models.user import User
from app.schemas.auth import (
    LoginRequest,
    RegisterRequest,
)


class AuthService:

    def __init__(self, db: Session):
        self.db = db

    def register(self, user: RegisterRequest):

        existing_user = (
            self.db.query(User)
            .filter(User.email == user.email)
            .first()
        )

        if existing_user:
            raise ValueError("Користувач вже існує")

        new_user = User(
            username=user.username,
            email=user.email,
            hashed_password=hash_password(user.password),
            first_name=user.first_name,
            last_name=user.last_name,
        )

        try:
            self.db.add(new_user)
            self.db.commit()
            self.db.refresh(new_user)

        except:
            self.db.rollback()
            raise

        return new_user

    def login(self, data: LoginRequest):

        user = (
            self.db.query(User)
            .filter(User.email == data.email)
            .first()
        )

        if not user:
            raise ValueError("Невірний email або пароль")

        if not verify_password(
            data.password,
            user.hashed_password
        ):
            raise ValueError("Невірний email або пароль")

        access_token = create_access_token(
            {"sub": str(user.id)}
        )

        refresh_token = create_refresh_token(
            {"sub": str(user.id)}
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role,
            }
        }