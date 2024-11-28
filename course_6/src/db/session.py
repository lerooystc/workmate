from contextlib import asynccontextmanager

from src.config import settings
from src.db.base import Base
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
from redis import asyncio as aioredis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from sqlalchemy.schema import CreateSchema

sync_engine = create_engine(settings.DB.get_postgres_url(is_async=False), echo=True)

sync_session = sessionmaker(sync_engine)

async_engine = create_async_engine(
    settings.DB.get_postgres_url(is_async=True), echo=True
)

async_session = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)


@asynccontextmanager
async def lifespan(_: FastAPI):
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.execute(CreateSchema("spimex_trades", if_not_exists=True))
        await conn.run_sync(Base.metadata.create_all)
    redis = aioredis.from_url(settings.DB.get_redis_url(), decode_responses=False)
    FastAPICache.init(
        RedisBackend(redis),
        prefix="fastapi-cache",
        cache_status_header="X-CustomCache-PleaseWork-Header",
    )
    yield


class SessionGetter:
    def __init__(self, start_async: bool):
        self.start_async = start_async

    async def __call__(self) -> Session:
        if self.start_async:
            async with async_session() as session:
                yield session
        else:
            with sync_session() as session:
                yield session
