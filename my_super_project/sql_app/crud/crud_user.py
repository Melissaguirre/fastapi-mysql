from sqlalchemy.orm import Session

from my_super_project.sql_app import models
from my_super_project.sql_app import schemas
from my_super_project.sql_app.models.user import User


def get_user(db: Session, user_id: int):
    return db.query(models.user.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.user.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.user.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.user.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.user.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

