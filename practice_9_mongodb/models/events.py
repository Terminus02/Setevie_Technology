from typing import List, Optional
from beanie import Document
from pydantic import BaseModel, ConfigDict, Field


class Event(Document):
    title: str
    image: str
    description: str
    tags: List[str]
    location: str

    class Settings:
        name = "events"

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Конференция по FastAPI",
                "image": "https://example.com/event.png",
                "description": "Практическая работа с MongoDB",
                "tags": ["python", "fastapi", "mongodb"],
                "location": "Москва"
            }
        }
    )


class EventCreate(BaseModel):
    title: str
    image: str
    description: str
    tags: List[str]
    location: str


class EventUpdate(BaseModel):
    title: Optional[str] = None
    image: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    location: Optional[str] = None
