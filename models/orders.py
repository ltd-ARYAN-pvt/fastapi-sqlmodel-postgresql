from typing import Optional
from sqlmodel import SQLModel, Field, Relationship


class Order(SQLModel, table=True):

    __tablename__ = "orders"

    id: Optional[int] = Field(default=None, primary_key=True)
    product: str
    user_id: int = Field(foreign_key="users.id")
    user: Optional["User"] = Relationship(back_populates="orders")