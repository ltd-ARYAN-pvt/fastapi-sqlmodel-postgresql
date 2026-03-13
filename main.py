from fastapi import FastAPI, Depends
from sqlmodel import Session, SQLModel
from routes import user, order
from core.database import engine

app = FastAPI(
    title="SQLModel + FastAPI + PostgreSQL",
    description="A simple example of using SQLModel with FastAPI and PostgreSQL.",
    version="v1.0.0"
)

app.include_router(user.router)
app.include_router(order.router)

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

@app.get("/ping")
def ping():
    return {"message": "Pong!"}