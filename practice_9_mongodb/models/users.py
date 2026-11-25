from typing import List
from beanie import Document, Link
from pydantic import BaseModel, EmailStr, Field

from models.events import Event


class User(Document):
    email: EmailStr
    password: str
    events: List[Link[Event]] = Field(default_factory=list)

    class Settings:
        name = "users"


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserSignIn(BaseModel):
    email: EmailStr
    password: str
