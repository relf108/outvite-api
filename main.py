import uvicorn
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from redis import asyncio as aioredis

from core.db import init_db
from handlers import auth_token, user

app = FastAPI()

app.include_router(auth_token.router)
app.include_router(user.router)


@cache()
async def get_cache():
    return 1


@app.get("/")
@cache(expire=60)
async def index():
    return dict(hello="world")


@app.on_event("startup")
async def start_db():
    await init_db()
    from datetime import datetime

    from model.user import User

    await User(
        email="tristan.sutton@gmail.com",
        first_name="Tristan",
        last_name="Sutton",
        DOB=datetime.now(),
        phone_number="0424415350",
    ).insert()


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url(
        "redis://localhost", encoding="utf8", decode_responses=True
    )
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


def main():
    uvicorn.run(app, host="127.0.0.1", port=8000)


if __name__ == "__main__":
    main()
