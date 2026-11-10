from pydantic import BaseModel, EmailStr, Field
from typing import List
from models.events import Event


class User(BaseModel):
    email: EmailStr
    password: str
    events: List[Event] = Field(default_factory=list)


class NewUser(User):
    username: str


class UserSignIn(BaseModel):
    email: EmailStr
    password: str
