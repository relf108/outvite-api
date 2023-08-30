import uvicorn
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from redis import asyncio as aioredis

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


# @app.on_event("startup")
# async def start_db():
#    await init_db()


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
