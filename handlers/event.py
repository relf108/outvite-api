from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from model.event import Event
from model.user import User, get_user

router = APIRouter()


@router.post("/events", response_model=Event)
async def create_event(event: Event, host: Annotated[User, Depends(get_user)]):
    if (await event.host.fetch()).id != host.id:
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to create an event on another user's behalf",
        )
    return await event.insert()


@router.put("/events", response_model=Event)
async def update_event(event: Event, host: Annotated[User, Depends(get_user)]):
    if (await Event.find_one(Event.id == event.id)) is None:
        raise HTTPException(status_code=400, detail="No existing event with that ID")
    if (await event.host.fetch()).id != host.id:
        raise HTTPException(
            status_code=403, detail="You are not the host of this event"
        )
    return await event.save()
