from typing import Annotated

from fastapi import APIRouter, Depends

from core.web import sensitive_fields
from model.event import Event
from model.user import User, get_user

router = APIRouter()


@router.post("/users/register", response_model=User)
@sensitive_fields(["hashed_password"])
async def register_user(user: User):
    return await user.register()


@router.get("/users/me/", response_model=User)
@sensitive_fields(["hashed_password"])
async def read_users_me(current_user: Annotated[User, Depends(get_user)]):
    return current_user


@router.get("/users/me/events/", response_model=list[Event])
async def get_user_events(current_user: Annotated[User, Depends(get_user)]):
    return await Event.find_many(Event.host == current_user).to_list()


@router.get("/users/me/events/attending", response_model=list[Event])
async def get_user_events_attending(current_user: Annotated[User, Depends(get_user)]):
    return await Event.find_many(current_user in Event.attendees).to_list()


@router.post("users/me/events", response_model=Event)
async def create_user_event(
    current_user: Annotated[User, Depends(get_user)], event: Event
):
    event.host = current_user
    return await event.create_event()
