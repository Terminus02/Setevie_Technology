from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str = "mongodb://127.0.0.1:27017/planner"

    model_config = SettingsConfigDict(env_file=".env")


client = None


async def initialize_database():
    global client

    from models.events import Event
    from models.users import User

    settings = Settings()

    client = AsyncIOMotorClient(settings.DATABASE_URL)

    await client.admin.command("ping")

    await init_beanie(
        database=client.get_default_database(),
        document_models=[Event, User]
    )

    print("MongoDB успешно подключена")


def close_database():
    global client

    if client is not None:
        client.close()
        client = None


from beanie import Document, PydanticObjectId
from pydantic import BaseModel


class Database:
    def __init__(self, model: type[Document]):
        self.model = model

    # Создание документа
    async def save(self, document):
        await document.create()
        return document

    # Получение документа по ID
    async def get(self, id: PydanticObjectId):
        return await self.model.get(id)

    # Получение всех документов
    async def get_all(self):
        return await self.model.find_all().to_list()

    # Обновление документа
    async def update(self, id: PydanticObjectId, body: BaseModel):
        document = await self.get(id)

        if document is None:
            return None

        update_data = body.model_dump(
            exclude_unset=True,
            exclude_none=True
        )

        if update_data:
            await document.set(update_data)

        return await self.get(id)

    # Удаление документа по ID
    async def delete(self, id: PydanticObjectId):
        document = await self.get(id)

        if document is None:
            return False

        await document.delete()
        return True

    # Удаление всех документов
    async def delete_all(self):
        await self.model.find_all().delete()
        return True
