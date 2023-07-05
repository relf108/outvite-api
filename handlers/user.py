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


@router.get("/users/me/events/hosting", response_model=list[Event])
async def get_user_events(current_user: Annotated[User, Depends(get_user)]):
    hosting_db: list[Event] = await Event.find_many(
        Event.host.id == current_user.id
    ).to_list()
    return hosting_db


@router.get("/users/me/events/attending", response_model=list[Event])
async def get_user_events_attending(current_user: Annotated[User, Depends(get_user)]):
    attending_db: list[Event] = await Event.find_many(
        Event.attendees.id == current_user.id
    ).to_list()
    return attending_db
