from fastapi import APIRouter, Depends
from sqlmodel import Session

from core.database import get_session
from schemas.user import UserCreate, UserRead
from models import User
from crud.user import (
    create_user,
    get_user,
    get_users_paginated,
    update_user,
    delete_user
)

router = APIRouter(prefix="/users", tags=["Users"])

#--> Create a new user
@router.post("/", response_model=UserRead)
def create_user_api(
    user: UserCreate,
    session: Session = Depends(get_session)
):
    db_user = User(**user.model_dump())
    return create_user(session, db_user)

#--> Get a user by ID
@router.get("/{user_id}", response_model=UserRead)
def read_user(
    user_id: int,
    session: Session = Depends(get_session)
):

    return get_user(session, user_id)

#--> Get users with pagination
@router.get("/", response_model=list[UserRead])
def read_users(
    offset: int = 0,
    limit: int = 10,
    session: Session = Depends(get_session)
):

    return get_users_paginated(session, offset, limit)

#--> Update an existing user
@router.put("/{user_id}", response_model=UserRead)
def update_user_api(
    user_id: int,
    user_update: UserCreate,
    session: Session = Depends(get_session)
):
    db_user = get_user(session, user_id)
    if not db_user:
        return None
    for key, value in user_update.model_dump().items():
        setattr(db_user, key, value)
    return update_user(session, db_user)

#--> Delete a user
@router.delete("/{user_id}", response_model=UserRead)
def delete_user_api(
    user_id: int,
    session: Session = Depends(get_session)
):
    db_user = get_user(session, user_id)
    if not db_user:
        return None
    return delete_user(session, db_user)