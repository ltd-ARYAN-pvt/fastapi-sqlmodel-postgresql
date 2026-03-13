from fastapi import APIRouter, Depends
from sqlmodel import Session

from core.database import get_session
from schemas.order import OrderCreate, OrderRead
from models import Order
from crud.order import (
    create_order,
    get_order,
    get_orders_paginated,
    update_order,
    delete_order
)

router = APIRouter(prefix="/orders", tags=["Orders"])

#--> Create a new order
@router.post("/", response_model=OrderRead)
def create_order_api(
    order: OrderCreate,
    session: Session = Depends(get_session)
):
    db_order = Order(**order.model_dump())
    return create_order(session, db_order)

#--> Get an order by ID
@router.get("/{order_id}", response_model=OrderRead)
def read_order(
    order_id: int,
    session: Session = Depends(get_session)
):

    return get_order(session, order_id)

#--> Get orders with pagination
@router.get("/", response_model=list[OrderRead])
def read_orders(
    offset: int = 0,
    limit: int = 10,
    session: Session = Depends(get_session)
):

    return get_orders_paginated(session, offset, limit)

#--> Update an existing order
@router.put("/{order_id}", response_model=OrderRead)
def update_order_api(
    order_id: int,
    order_update: OrderCreate,
    session: Session = Depends(get_session)
):
    db_order = get_order(session, order_id)
    if not db_order:
        return None
    for key, value in order_update.model_dump().items():
        setattr(db_order, key, value)
    return update_order(session, db_order)

#--> Delete an order
@router.delete("/{order_id}", response_model=OrderRead)
def delete_order_api(
    order_id: int,
    session: Session = Depends(get_session)
):
    db_order = get_order(session, order_id)
    if not db_order:
        return None
    return delete_order(session, db_order)