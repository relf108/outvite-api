from datetime import datetime
from typing import Self

from beanie import Document, Link, PydanticObjectId
from pydantic import BaseModel

from model.user import User


class Event(Document):
    host: Link[User]
    name: str
    location: str
    start_time: datetime
    end_time: datetime
    description: str
    attendees: list[Link[User]]

    async def create_event(self):
        return await self.insert()

    async def update_event(self, event: Self):
        for key, value in await event:
            if key not in ["id", "host"]:
                setattr(self, key, value)
        return await self.save()
