from typing import List, Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    name: str


class PasswordBase(BaseModel):
    value: str


class User(UserBase):
    id: int
    points: int

    class Config:
        orm_mode = True


class TaskBase(BaseModel):
    task_id: int
    reference: str
    answer: str
