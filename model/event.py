from datetime import datetime

from beanie import Document

from model.user import User


class Event(Document):
    host: User
    namee: str
    location: str
    start_time: datetime
    end_time: datetime
    description: str
    attendees: list[User]

    async def create_event(self):
        await self.insert()
        return self
