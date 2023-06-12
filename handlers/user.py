from typing import Annotated

from fastapi import APIRouter, Depends
from core.web import sensitive_fields

from model.user import User, get_current_user

router = APIRouter()


@router.get("/users/me/", response_model=User)
@sensitive_fields(["hashed_password"])
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user


@router.post("/users/register", response_model=User)
@sensitive_fields(["hashed_password"])
async def register_user(user: User):
    await user.register()
    return user
