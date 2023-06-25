from datetime import datetime
from typing import Self

from beanie import Document, PydanticObjectId
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
        await self.insert()
        return EventJSON.from_event(self)

    async def update_event(self, event: Self):
        for key, value in (await event):
            if key not in ["id", "host"]:
                setattr(self, key, value)
        await self.save()
        return EventJSON.from_event(await Event.get(self.id))


class EventJSON(BaseModel):
    id: PydanticObjectId = None
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

    def from_event(event: Event) -> Self:
        return EventJSON(
            id=event.id,
            name=event.name,
            location=event.location,
            start_time=event.start_time,
            end_time=event.end_time,
            description=event.description,
            attendees=[attendee.email for attendee in event.attendees],
        )
