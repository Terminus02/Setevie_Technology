from fastapi import FastAPI
from routes.users import user_router
from routes.events import event_router

app = FastAPI(
    title="Планировщик событий",
    description="Практическая работа по структурированию FastAPI",
    version="1.0"
)

app.include_router(user_router, prefix="/user")
app.include_router(event_router, prefix="/event")


@app.get("/")
async def welcome():
    return {
        "message": "Приложение планировщика успешно работает"
    }
