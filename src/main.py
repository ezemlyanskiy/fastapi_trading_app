from fastapi import FastAPI
from fastapi_cache import FastAPICache
# from contextlib import asynccontextmanager  # Update later
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from fastapi.middleware.cors import CORSMiddleware

from src.auth.base_config import auth_backend, fastapi_users
from src.auth.schemas import UserRead, UserCreate
from src.operations.router import router as operation_router
from src.tasks.router import router as tasks_router
from src.config import REDIS_HOST


# @asynccontextmanager  # Update later
# async def lifespan(app: FastAPI):
#     redis = aioredis.from_url(
#         f"redis://{REDIS_HOST}",
#         encoding="utf8",
#         decode_responses=True
#     )
#     FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
#     yield


app = FastAPI(
    title="Trading App",
    # lifespan=lifespan,  # Update later
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(operation_router)
app.include_router(tasks_router)


origins = [
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization",
    ],
)


@app.on_event("startup")
async def startup_event():
    redis = aioredis.from_url(
        f"redis://{REDIS_HOST}", encoding="utf8", decode_responses=True
    )
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
