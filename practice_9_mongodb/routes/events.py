from fastapi import APIRouter, HTTPException, status
from beanie import PydanticObjectId

from database.connection import Database
from models.events import Event, EventCreate, EventUpdate


event_router = APIRouter(tags=["Events"])
event_database = Database(Event)


# Получить список всех событий
@event_router.get("/", response_model=list[Event])
async def retrieve_all_events():
    return await event_database.get_all()


# Создать новое событие
@event_router.post("/new", status_code=201)
async def create_event(body: EventCreate):
    new_event = Event(**body.model_dump())

    await event_database.save(new_event)

    return {
        "message": "Event created successfully",
        "id": str(new_event.id)
    }


# Удалить все события
@event_router.delete("/")
async def delete_all_events():
    await event_database.delete_all()

    return {
        "message": "Events deleted successfully"
    }


# Получить событие по ID
@event_router.get("/{id}", response_model=Event)
async def retrieve_event(id: PydanticObjectId):
    event = await event_database.get(id)

    if event is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event with supplied ID does not exist"
        )

    return event


# Изменить событие по ID
@event_router.put("/{id}", response_model=Event)
async def update_event(
    id: PydanticObjectId,
    body: EventUpdate
):
    updated_event = await event_database.update(id, body)

    if updated_event is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event with supplied ID does not exist"
        )

    return updated_event


# Удалить событие по ID
@event_router.delete("/{id}")
async def delete_event(id: PydanticObjectId):
    deleted = await event_database.delete(id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event with supplied ID does not exist"
        )

    return {
        "message": "Event deleted successfully"
    }
