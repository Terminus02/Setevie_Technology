from pydantic import BaseModel, ConfigDict
from typing import List


class Event(BaseModel):
    id: int
    title: str
    image: str
    description: str
    tags: List[str]
    location: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": 1,
                "title": "FastAPI Book Launch",
                "image": "https://example.com/image.png",
                "description": "Presentation of the FastAPI book",
                "tags": ["python", "fastapi", "book"],
                "location": "Google Meet"
            }
        }
    )
