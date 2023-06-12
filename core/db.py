from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from model.event import Event
from model.user import User


async def init_db():
    CONNECTION_STRING = "mongodb://localhost/outvite"
    client = AsyncIOMotorClient(CONNECTION_STRING)
    await init_beanie(database=client["outvite"], document_models=[User, Event])
