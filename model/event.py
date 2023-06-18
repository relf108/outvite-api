from datetime import datetime

from beanie import Document
from pydantic import BaseModel

from model.user import User


class Event(Document):
    host: User
    name: str
    location: str
    start_time: datetime
    end_time: datetime
    description: str
    attendees: list[User]

    async def create_event(self):
        return await self.insert()


class EventJSON(BaseModel):
    name: str
    location: str
    start_time: datetime
    end_time: datetime
    description: str
    attendees: list[str]

    async def as_event(self, host: User) -> Event:
        return Event(
            host=host,
            name=self.name,
            location=self.location,
            start_time=self.start_time,
            end_time=self.end_time,
            description=self.description,
            attendees=[
                await User.find_one(User.email == attendee)
                for attendee in self.attendees
            ],
        )
