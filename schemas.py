from typing import List, Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    name: str


class User(UserBase):
    id: int
    points: int

    class Config:
        orm_mode = True
