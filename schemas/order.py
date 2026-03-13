from sqlmodel import SQLModel


class OrderBase(SQLModel):
    product: str
    user_id: int

class OrderCreate(OrderBase):
    pass

class OrderRead(OrderBase):
    id: int