from datetime import datetime
from typing import Annotated

from beanie import Document, Indexed
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from core.web import sensitive_fields

from model.auth_token import ALGORITHM, SECRET_KEY, TokenData


class User(Document):
    email: Indexed(str)
    first_name: str
    last_name: str
    DOB: datetime
    phone_number: str
    hashed_password: str | None = None

    async def register(self):
        self.hashed_password = get_password_hash(self.hashed_password)
        await self.insert()
        return self


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = await User.find_one(User.email == token_data.email)
    if user is None:
        raise credentials_exception
    return user


async def authenticate_user(email: str, password: str):
    user = await User.find_one(User.email == email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user
