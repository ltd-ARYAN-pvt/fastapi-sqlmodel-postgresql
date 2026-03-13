from sqlmodel import SQLModel
from typing import Optional


class UserBase(SQLModel):
    name: str
    email: str
    age: Optional[int] = None


class UserCreate(UserBase):
    pass

#--> Optional fields for updating a user
class UserUpdate(SQLModel):
    name: str | None = None
    email: str | None = None

#--> Response model for user data
class UserRead(UserBase):
    id: int