from datetime import datetime
from typing import Annotated, Optional
from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from core import db
from core.db import Base
from model.auth_token import ALGORITHM, SECRET_KEY, TokenData
from pydantic import BaseModel


class UserDao(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    first_name: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    last_name: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    dob: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    hashed_password: Mapped[Optional[str]] = mapped_column(String(100), nullable=False)


class UserModel(BaseModel):
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    dob: Optional[datetime] = None
    hashed_password: Optional[str] = None


class UserObject(object):
    def to_response_model(self, user: UserDao) -> UserModel:
        return UserModel(
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            dob=user.dob,
        )

    def insert(self, user: UserDao):
        with db.get_session() as session:
            session.add(user)
            session.commit()

    def update(self, user: UserDao):
        with db.get_session() as session:
            session.merge(user)
            session.commit()

    def delete(self, user: UserDao):
        with db.get_session() as session:
            session.delete(user)
            session.commit()

    def get(self, user: UserModel) -> list[UserDao]:
        filters: list = []
        for key, value in user.dict().items():
            if value:
                filters.append(getattr(UserDao, key) == value)
        with db.get_session() as session:
            return session.query(UserDao).filter(*filters).all()

    def register(self, user: UserModel):
        db_user = UserDao(**user.dict())
        db_user.hashed_password = get_password_hash(user.hashed_password)
        UserObject().insert(db_user)
        return self.to_response_model(db.get_session().merge(db_user))


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_auth_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = str(payload.get("sub"))
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = UserObject().get(UserModel(email=token_data.email or ""))
    if len(user) == 0:
        raise credentials_exception
    return UserObject().to_response_model(user[0])


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def authenticate_user(email: str, password: str):
    user = UserObject().get(UserModel(email=email))[0]
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user
