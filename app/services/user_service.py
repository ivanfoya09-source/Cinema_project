from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.user import User
from app.schemas.user import UserCreate

from .base_service import BaseService


class UserService(BaseService):

    def __init__(self, db: Session):
        super().__init__(db)

    def get_all(self):
        return self.db.query(User).all()

    def get_by_id(self, user_id: int):
        return (
            self.db.query(User)
            .filter(User.id == user_id)
            .first()
        )

    def get_by_email(self, email: str):
        return (
            self.db.query(User)
            .filter(User.email == email)
            .first()
        )

    def get_by_username(self, username: str):
        return (
            self.db.query(User)
            .filter(User.username == username)
            .first()
        )

    def create(self, user: UserCreate):

        if self.get_by_email(user.email):
            raise ValueError("Email вже використовується")

        if self.get_by_username(user.username):
            raise ValueError("Username вже використовується")

        db_user = User(
            username=user.username,
            email=user.email,
            hashed_password=hash_password(user.password),
            first_name=user.first_name,
            last_name=user.last_name,
            phone=user.phone,
            birth_date=user.birth_date,
            city=user.city,
            avatar=user.avatar,
        )

        return self.add(db_user)

    def update(self, user: User, data: dict):

        for key, value in data.items():

            if value is None:
                continue

            if key == "password":
                key = "hashed_password"
                value = hash_password(value)

            setattr(user, key, value)

        try:
            self.commit()
            self.refresh(user)

        except Exception:
            self.db.rollback()
            raise

        return user