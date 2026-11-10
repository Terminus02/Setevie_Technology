from contextlib import asynccontextmanager
from fastapi import FastAPI

from database.connection import conn
from routes.users import user_router
from routes.events import event_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    conn()
    yield


app = FastAPI(
    title="Планировщик событий",
    description="Практическая работа №8. SQLite и SQLModel",
    version="2.0",
    lifespan=lifespan
)

app.include_router(user_router, prefix="/user")
app.include_router(event_router, prefix="/event")


@app.get("/")
async def welcome():
    return {
        "message": "Планировщик событий работает с SQLite"
    }
