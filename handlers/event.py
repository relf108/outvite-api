from typing import Annotated
from fastapi import APIRouter, Depends
from core.web import sensitive_fields
from model.event import Event, EventJSON
from model.user import User, get_user

router = APIRouter()


@router.post("/events", response_model=EventJSON)
async def create_event(event: EventJSON, host: Annotated[User, Depends(get_user)]):
    db_event = await event.as_event(host)
    await db_event.create_event()
    return event
