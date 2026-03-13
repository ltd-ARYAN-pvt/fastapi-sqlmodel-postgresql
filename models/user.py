from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from models.base import TimestampMixin


class User(TimestampMixin, SQLModel, table=True):

    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    email: str = Field(unique=True, index=True)
    age: Optional[int] = None
    orders: List["Order"] = Relationship(back_populates="user")