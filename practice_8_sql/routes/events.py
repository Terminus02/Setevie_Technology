from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from database.connection import get_session
from models.events import Event, EventCreate, EventUpdate


event_router = APIRouter(tags=["Events"])


# Получить все события
@event_router.get("/", response_model=list[Event])
async def retrieve_all_events(
    session: Session = Depends(get_session)
):
    events = session.exec(select(Event)).all()
    return events


# Получить событие по ID
@event_router.get("/{id}", response_model=Event)
async def retrieve_event(
    id: int,
    session: Session = Depends(get_session)
):
    event = session.get(Event, id)

    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event with supplied ID does not exist"
        )

    return event


# Создать новое событие
@event_router.post("/new", status_code=201)
async def create_event(
    event: EventCreate,
    session: Session = Depends(get_session)
):
    new_event = Event(**event.model_dump())

    session.add(new_event)
    session.commit()
    session.refresh(new_event)

    return {
        "message": "Event created successfully",
        "id": new_event.id
    }


# Обновить существующее событие
@event_router.put("/edit/{id}", response_model=Event)
async def update_event(
    id: int,
    new_data: EventUpdate,
    session: Session = Depends(get_session)
):
    event = session.get(Event, id)

    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event with supplied ID does not exist"
        )

    event_data = new_data.model_dump(exclude_unset=True)

    for key, value in event_data.items():
        setattr(event, key, value)

    session.add(event)
    session.commit()
    session.refresh(event)

    return event


# Удалить событие по ID
@event_router.delete("/delete/{id}")
@event_router.delete("/{id}", include_in_schema=False)
async def delete_event(
    id: int,
    session: Session = Depends(get_session)
):
    event = session.get(Event, id)

    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event with supplied ID does not exist"
        )

    session.delete(event)
    session.commit()

    return {
        "message": "Event deleted successfully"
    }


# Удалить все события
@event_router.delete("/")
async def delete_all_events(
    session: Session = Depends(get_session)
):
    events = session.exec(select(Event)).all()

    for event in events:
        session.delete(event)

    session.commit()

    return {
        "message": "Events deleted successfully"
    }
