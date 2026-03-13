from sqlmodel import Session, select 
from models import Order

#--> Create a new order
def create_order(session: Session, order: Order):
    session.add(order)
    session.commit()
    session.refresh(order)
    return order

#--> Get an order by ID
def get_order(session: Session, order_id: int):
    statement = select(Order).where(Order.id == order_id)
    return session.exec(statement).first()

#--> Get all orders
def get_orders(session: Session):
    statement = select(Order)
    return session.exec(statement).all()

#--> Get orders with pagination
#--> This function retrieves a subset of orders based on the specified offset and limit.
def get_orders_paginated(session: Session, offset: int = 0, limit: int = 10):
    statement = select(Order).offset(offset).limit(limit)
    return session.exec(statement).all()

#--> Update an existing order
def update_order(session: Session, order: Order):
    session.add(order)
    session.commit()
    session.refresh(order)
    return order

#--> Delete an order
def delete_order(session: Session, order: Order):
    session.delete(order)
    session.commit()
    return order