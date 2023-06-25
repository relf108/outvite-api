from typing import Annotated

from fastapi import APIRouter, Depends

from core.web import sensitive_fields
from model.event import Event, EventJSON
from model.user import User, get_user
from beanie.odm.operators.find.array import ElemMatch

router = APIRouter()


@router.post("/users/register", response_model=User)
@sensitive_fields(["hashed_password"])
async def register_user(user: User):
    return await user.register()


@router.get("/users/me/", response_model=User)
@sensitive_fields(["hashed_password"])
async def read_users_me(current_user: Annotated[User, Depends(get_user)]):
    return current_user


@router.get("/users/me/events/hosting", response_model=list[EventJSON])
async def get_user_events(current_user: Annotated[User, Depends(get_user)]):
    hosting_db: list[Event] = await Event.find_many(
        Event.host == current_user
    ).to_list()
    return [EventJSON.from_event(rec) for rec in hosting_db]


@router.get("/users/me/events/attending", response_model=list[EventJSON])
async def get_user_events_attending(current_user: Annotated[User, Depends(get_user)]):
    attending_db: list[Event] = await Event.find_many(
        ElemMatch(Event.attendees, current_user)
    ).to_list()
    return [EventJSON.from_event(rec) for rec in attending_db]
