from contextlib import asynccontextmanager

from fastapi import FastAPI

from database.connection import initialize_database, close_database
from routes.users import user_router
from routes.events import event_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await initialize_database()
    yield
    close_database()


app = FastAPI(
    title="Планировщик событий",
    description="Практическая работа №9. MongoDB и Beanie",
    version="3.0",
    lifespan=lifespan
)

app.include_router(user_router, prefix="/user")
app.include_router(event_router, prefix="/event")


@app.get("/")
async def welcome():
    return {
        "message": "Планировщик событий работает с MongoDB"
    }
