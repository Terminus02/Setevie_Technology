from typing import List, Optional
from sqlalchemy import Column, JSON
from sqlmodel import SQLModel, Field


class Event(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    image: str
    description: str
    tags: List[str] = Field(sa_column=Column(JSON))
    location: str


class EventCreate(SQLModel):
    title: str
    image: str
    description: str
    tags: List[str]
    location: str


class EventUpdate(SQLModel):
    title: Optional[str] = None
    image: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    location: Optional[str] = None
