from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from my_super_project.sql_app.crud import crud_user
from my_super_project.sql_app.crud import crud_item
from my_super_project.sql_app.schemas.user import User
from my_super_project.sql_app.schemas.item import Item
from . import  models, schemas
from my_super_project.sql_app.db.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users",
    response_model=schemas.user.User,
    tags = ["Users"])
def create_user(user: schemas.user.UserCreate, db: Session = Depends(get_db)):
    db_user = crud_user.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud_user.create_user(db=db, user=user)


@app.get("/users", 
    response_model=List[schemas.user.User], 
    tags = ["Users"])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)) -> List[User]:
    users = crud_user.get_users(db, skip=skip, limit=limit) 
    return users


@app.get("/users/{user_id}", 
    response_model=schemas.user.User,
    tags = ["Users"])
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud_user.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/items", 
    response_model=schemas.item.Item,
    tags = ["Items"])
def create_item_for_user(
    user_id: int, item: schemas.item.ItemCreate, db: Session = Depends(get_db)
):
    return crud_item.create_user_item(db=db, item=item, user_id=user_id)


@app.get("/items", 
    response_model=List[schemas.item.Item],
    tags = ["Items"]) 
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)) -> List[Item]: 
    items = crud_item.get_items(db, skip=skip, limit=limit)
    return items