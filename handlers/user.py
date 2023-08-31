from typing import Annotated

from fastapi import APIRouter, Depends

from core.web import sensitive_fields
from model.user import UserObject, get_auth_user, UserModel

router = APIRouter()


@router.post("/users/register", response_model=UserModel)
@sensitive_fields(["hashed_password"])
async def register_user(user: UserModel):
    resp = UserObject().register(user)
    return resp


@router.get("/users/me/", response_model=UserModel)
@sensitive_fields(["hashed_password"])
async def read_users_me(current_user: Annotated[UserModel, Depends(get_auth_user)]):
    return current_user
