from sqlalchemy.orm import Session


class BaseService:

    def __init__(self, db: Session):
        self.db = db

    def add(self, obj):

        try:
            self.db.add(obj)
            self.db.commit()
            self.db.refresh(obj)

            return obj

        except Exception:
            self.db.rollback()
            raise

    def delete(self, obj):

        try:
            self.db.delete(obj)
            self.db.commit()

        except Exception:
            self.db.rollback()
            raise

    def commit(self):

        try:
            self.db.commit()

        except Exception:
            self.db.rollback()
            raise

    def refresh(self, obj):
        self.db.refresh(obj)