from datetime import datetime

from beanie import Document, Link

from model.user import User


class Event(Document):
    host: Link[User]
    name: str
    location: str
    start_time: datetime
    end_time: datetime
    description: str
    attendees: list[Link[User]]
