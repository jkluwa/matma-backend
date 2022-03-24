from cgitb import text
from sqlalchemy.orm import Session
import random

import models
import schemas


def get_user(db: Session, user_name: int):
    return db.query(models.User).filter(models.User.name == user_name).first()


def get_user_by_name(db: Session, name: str):
    return db.query(models.User).filter(models.User.name == name).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserBase):
    db_user = models.User(name=user.name, points=0)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)


def get_task(db: Session):
    return db.query(models.Task)[random.randrange(0, db.query(models.Task).count())]
