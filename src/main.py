from fastapi import FastAPI
from fastapi_cache import FastAPICache
from contextlib import asynccontextmanager
from fastapi_cache.backends.redis import RedisBackend

from redis import asyncio as aioredis
from .auth.base_config import auth_backend, fastapi_users
from .auth.schemas import UserRead, UserCreate
from .operations.router import router as operation_router
from .tasks.router import router as tasks_router
from .config import REDIS_HOST, REDIS_PORT


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = aioredis.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield


app = FastAPI(
    title="Trading App",
    lifespan=lifespan,
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
