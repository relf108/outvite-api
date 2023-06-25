from typing import Annotated

from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, HTTPException
from model.event import Event, EventJSON
from model.user import User, get_user

router = APIRouter()


@router.post("/events", response_model=EventJSON)
async def create_event(event: EventJSON, host: Annotated[User, Depends(get_user)]):
    db_event = await event.as_event(host)
    return await db_event.create_event()


@router.put("/events", response_model=EventJSON)
async def update_event(event: EventJSON, host: Annotated[User, Depends(get_user)]):
    db_event = await Event.get(event.id)
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")
    if db_event.host != host:
        raise HTTPException(
            status_code=403, detail="You are not the host of this event"
        )
    return await db_event.update_event(event.as_event(host))
