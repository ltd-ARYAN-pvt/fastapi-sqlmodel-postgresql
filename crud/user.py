from sqlmodel import Session, select
from models import User

#--> Create a new user
def create_user(session: Session, user: User):
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

#--> Get a user by ID
def get_user(session: Session, user_id: int):
    statement = select(User).where(User.id == user_id)
    return session.exec(statement).first()

#--> Get all users
def get_users(session: Session):
    statement = select(User)
    return session.exec(statement).all()

#--> Get users with pagination
#--> This function retrieves a subset of users based on the specified offset and limit.
def get_users_paginated(session: Session, offset: int = 0, limit: int = 10):
    statement = select(User).offset(offset).limit(limit)
    return session.exec(statement).all()

#--> Update an existing user
def update_user(session: Session, user: User):
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

#--> Delete a user
def delete_user(session: Session, user: User):
    session.delete(user)
    session.commit()
    return user