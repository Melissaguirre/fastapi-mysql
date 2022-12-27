from sqlalchemy.orm import Session

from my_super_project.sql_app import models
from my_super_project.sql_app import schemas
from my_super_project.sql_app.models.item import Item

def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.item.ItemCreate, user_id: int):
    db_item = models.item.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
